"""Rebuild normalized working task files from the immutable release.

Only mechanical transformations: order-preserving tool de-duplication, unique
verifier identifiers and integer typing for direct SQL COUNT expectations.
SQL, comparison operators, task text, membership and expected magnitudes stay fixed.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import sys
import sqlglot
from sqlglot import exp

ROOT=Path(__file__).resolve().parents[1]

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def writej(p,x): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def writejl(p,rows): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))

def is_direct_count(query):
    try:
        parsed=sqlglot.parse_one(query,read='sqlite')
    except Exception:
        return False
    if not isinstance(parsed,exp.Select) or len(parsed.expressions)!=1: return False
    expression=parsed.expressions[0]
    if isinstance(expression,exp.Alias): expression=expression.this
    return isinstance(expression,exp.Count)

def normalize(record):
    obj=json.loads(json.dumps(record));changes=[]
    for field in ['selected_tools','restricted_tools']:
        original=obj[field];dedup=list(dict.fromkeys(original))
        if dedup!=original:
            obj[field]=dedup
            changes.append({'path':field,'before':original,'after':dedup,'kind':'deduplicate_tool_names_preserving_order'})
    for index,v in enumerate(obj['verifiers']):
        old=v.get('name','')
        new=f'check-{index:04d}: {old}'
        v['name']=new
        changes.append({'path':f'verifiers[{index}].name','before':old,'after':new,'kind':'unique_verifier_identity'})
        cfg=v.get('validation_config',{})
        expected=cfg.get('expected_value')
        if (cfg.get('comparison_type','equals') in {'equals','greater_than','less_than'}
                and isinstance(expected,str) and re.fullmatch(r'[+-]?\d+',expected.strip())
                and is_direct_count(cfg.get('query',''))):
            cfg['expected_value']=int(expected)
            changes.append({'path':f'verifiers[{index}].validation_config.expected_value',
                            'before':expected,'after':int(expected),'kind':'direct_count_numeric_type_only'})
    return obj,changes

def main():
    source=ROOT/'data/source_release'
    manifest=json.loads((source/'split_manifest.json').read_text())
    all_changes=[];hashes={};counts={}
    allowed=('task_id','domain','system_prompt','user_prompt','selected_tools','restricted_tools')
    for role in ['train','development','final_test']:
        old=[json.loads(x) for x in (source/'evaluator_only'/f'{role}.jsonl').read_text().splitlines()]
        rows=[]
        for r in old:
            new,changes=normalize(r)
            assert len(new['verifiers'])==len(r['verifiers'])
            assert len({x['name'] for x in new['verifiers']})==len(new['verifiers'])
            for a,b in zip(r['verifiers'],new['verifiers']):
                assert a['validation_config']['query']==b['validation_config']['query']
                assert a['validation_config'].get('comparison_type','equals')==b['validation_config'].get('comparison_type','equals')
            assert new['user_prompt']==r['user_prompt'] and new['system_prompt']==r['system_prompt']
            rows.append(new)
            for c in changes: all_changes.append({'role':role,'task_id':r['task_id'],**c})
        assert {r['task_id'] for r in rows}==set(manifest['task_ids'][role])
        ep=ROOT/'data/evaluator_only'/f'{role}.jsonl'
        ip=ROOT/'data/task_inputs'/f'{role}.jsonl'
        writejl(ep,rows);writejl(ip,[{k:r[k] for k in allowed} for r in rows])
        for p in [ep,ip]: hashes[str(p.relative_to(ROOT))]=sha(p)
        counts[role]=len(rows)
    changes_path=ROOT/'data/metadata/normalization_changes.jsonl'
    writejl(changes_path,all_changes)
    counts_by_kind=dict(Counter(c['kind'] for c in all_changes))
    writej(ROOT/'data/metadata/normalization_manifest.json',{
        'version':'mechanical-normalization-v1','source_release_sha256':sha(source/'split_manifest.json'),
        'source_release_unchanged':True,'task_counts':counts,'task_membership_changed':False,
        'sql_queries_or_operators_changed':False,'change_counts':counts_by_kind,
        'changes_file_sha256':sha(changes_path),'working_file_sha256':hashes,
        'cleaner_sha256':sha(__file__),'sqlglot_version':sqlglot.__version__,
        'scope':'Representation normalization only. Runtime schemas and semantic task feasibility are not certified.'})
    writej(ROOT/'data/metadata/quality_holds.json',{
        'membership_retained':True,
        'tasks':[{'task_id':'task_20260115_154856_907_1628b966_275e920f','role':'final_test',
                  'status':'SEMANTIC_SCORER_REVIEW_REQUIRED',
                  'reason':'Verifier coverage and an unrequested open-case-count threshold may not match the task. Numeric string was normalized without changing the threshold; no new SQL or gold solution was invented.',
                  'action':'Do not silently score/drop/replace this task. Resolve the scorer against the task and backend before a final benchmark claim.'}],
        'other_tasks':'No exhaustive semantic-feasibility guarantee; runtime tool/schema checks still required.'})
    print(json.dumps({'working_counts':counts,'changes':counts_by_kind,'known_semantic_holds':1},indent=2))

if __name__=='__main__': main()

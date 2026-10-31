#!/usr/bin/env python3
"""Static audit only: no API, GPU, Docker, SQL execution, or model calls.

Core uses Python standard library. Optional sqlglot==30.6.0 performs SQLite
syntax/AST checks; its absence is explicitly reported, never called a pass.
Source task specifications remain unchanged. Verifier metadata is curator-only.
"""
from __future__ import annotations
import argparse, collections, copy, datetime, hashlib, json, math, os, re, sys, unicodedata
from pathlib import Path
from urllib.parse import urlparse
try:
    import sqlglot
    from sqlglot import exp
except ImportError:
    sqlglot = None
    exp = None

ROLES = ('train', 'development', 'final_test')
INPUT_FIELDS = {'task_id','domain','system_prompt','user_prompt','selected_tools','restricted_tools'}
FULL_FIELDS = INPUT_FIELDS | {'mcp_endpoint','number_of_runs','reset_database_between_runs','gym_servers_config','verifiers'}
EXPECTED_DOMAINS = {'calendar','csm','drive','email','hr','hybrid','itsm','teams'}

def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p): return sha_bytes(p.read_bytes())
def canonical(x): return json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(',',':'), allow_nan=False)
def normalize_text(x): return ' '.join(unicodedata.normalize('NFKC', x).casefold().split())
def hash_text(x): return sha_bytes(x.encode())

class Audit:
    def __init__(self): self.findings=[]; self.checks=collections.Counter(); self.inventory=[]
    def finding(self, code, severity, message, **context):
        self.findings.append({'code':code,'severity':severity,'message':message,**context})
    def check(self, condition, code, message, **context):
        self.checks[code]+=1
        if not condition: self.finding(code,'error',message,**context)
        return condition
    def decode(self,text,where):
        duplicates=[]
        def pairs(items):
            d={}
            for k,v in items:
                if k in d: duplicates.append(k)
                d[k]=v
            return d
        def bad_constant(v): raise ValueError('nonstandard JSON constant '+v)
        try:
            obj=json.loads(text,object_pairs_hook=pairs,parse_constant=bad_constant)
        except (ValueError,TypeError) as e:
            self.finding('invalid_json','error',str(e),location=where);return None
        if duplicates:self.finding('duplicate_json_keys','error','Duplicate JSON keys would overwrite values.',location=where,keys=sorted(set(duplicates)))
        return obj
    def readj(self,p):
        if not p.is_file():self.finding('missing_file','error','Required file missing.',path=str(p));return None
        return self.decode(p.read_text(),str(p))
    def readjl(self,p):
        if not p.is_file():self.finding('missing_file','error','Required JSONL missing.',path=str(p));return []
        out=[]
        with p.open() as f:
            for n,line in enumerate(f,1):
                if not line.strip():self.finding('blank_jsonl_line','warning','Blank JSONL line.',path=str(p),line=n);continue
                obj=self.decode(line,f'{p}:{n}')
                if isinstance(obj,dict):out.append(obj)
                elif obj is not None:self.finding('record_not_object','error','JSONL record must be an object.',path=str(p),line=n)
        return out

def sql_info(query):
    info={'parser':'sqlglot' if sqlglot else None,'parse_status':'not_checked','statement_count':None,'statement_types':[],'table_names':[], 'canonical_sql_sha256':None,'volatile_query':bool(re.search(r'\b(random|randomblob|current_timestamp|current_date|current_time)\b|[\'\"]now[\'\"]',query,re.I))}
    if not sqlglot:return info, None
    try:
        raw_trees=[t for t in sqlglot.parse(query,read='sqlite',error_level=sqlglot.ErrorLevel.RAISE) if t is not None]
        # SQLGlot emits comment-only Semicolon nodes after a trailing semicolon.
        # They are separators/comments, not executable SQL statements.
        trees=[t for t in raw_trees if not isinstance(t,exp.Semicolon)]
        info['ignored_comment_semicolon_nodes']=len(raw_trees)-len(trees)
        info['parse_status']='parsed';info['statement_count']=len(trees);info['statement_types']=[type(t).__name__ for t in trees]
        info['table_names']=sorted({t.name for tree in trees for t in tree.find_all(exp.Table)})
        # Equality here is normalized AST serialization, not arbitrary semantic equivalence.
        normalized=';'.join(t.sql(dialect='sqlite',normalize=True,comments=False) for t in trees)
        info['canonical_sql_sha256']=hash_text(normalized)
        info['read_query_only']=bool(trees) and all(isinstance(t,exp.Query) for t in trees)
        info['direct_scalar_count']=False
        if len(trees)==1 and isinstance(trees[0],exp.Select) and len(trees[0].expressions)==1 and trees[0].args.get('group') is None:
            value=trees[0].expressions[0]
            if isinstance(value,exp.Alias):value=value.this
            info['direct_scalar_count']=isinstance(value,exp.Count)
    except Exception as e:
        info['parse_status']='parse_error';info['parser_error_type']=type(e).__name__
        # Full parser messages often contain source SQL; keep them out of the general report.
        info['parser_error_sha256']=hash_text(str(e))
    return info, None

def main():
    here=Path(__file__).resolve();modal_root=here.parents[1];project_root=modal_root.parent
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset',type=Path,default=modal_root/'data/source_release')
    parser.add_argument('--payload-root',type=Path,default=None,help='Optional working task_inputs/evaluator_only root; frozen manifest/checksums still come from --dataset.')
    parser.add_argument('--report-dir',type=Path,default=modal_root/'reports')
    parser.add_argument('--inventory',type=Path,default=modal_root/'data/metadata/verifier_inventory.jsonl')
    parser.add_argument('--source-parquet-dir',type=Path,default=project_root/'work/enterpriseops-oracle',help='Hash-only source check; no parquet dependency or payload read.')
    parser.add_argument('--family-audit',type=Path,action='append',default=[])
    args=parser.parse_args();a=Audit();base=args.dataset.resolve();payload=args.payload_root.resolve() if args.payload_root else base
    manifest=a.readj(base/'split_manifest.json') or {};groups=a.readj(base/'workflow_groups.json') or {};checksums=a.readj(base/'checksums.json') or {}
    rows={};role_ids={};domain_counts={};tool_names=collections.Counter();schema_keys=collections.Counter();comparison_types=collections.Counter();expected_types=collections.Counter();query_status=collections.Counter();stats=collections.Counter();name_affected=set();name_loss_tasks=set();duplicate_check_tasks=set();query_conflict_tasks=set();prompt_buckets=collections.defaultdict(list);tool_signatures=collections.defaultdict(set)
    # All payload exports are checked against frozen hashes before parsing content.
    for relative,expected in checksums.items():
        path=base/relative
        a.check(path.is_file() and sha_file(path)==expected,'release_checksum','File differs from frozen release checksum.',file=relative)
    for relative,expected in manifest.get('export_sha256',{}).items():
        p=base/relative;a.check(p.is_file() and sha_file(p)==expected,'payload_checksum','Task payload differs from frozen manifest.',file=relative)
    source_hashes={}
    for filename,expected in manifest.get('source_parquet_sha256',{}).items():
        p=args.source_parquet_dir/filename
        if p.is_file():
            actual=sha_file(p);source_hashes[filename]={'status':'match' if actual==expected else 'mismatch','actual_sha256':actual};a.check(actual==expected,'source_parquet_checksum','Source parquet hash differs.',file=filename)
        else:source_hashes[filename]={'status':'not_available','expected_sha256':expected}
    for role in ROLES:
        full=a.readjl(payload/'evaluator_only'/f'{role}.jsonl');inputs=a.readjl(payload/'task_inputs'/f'{role}.jsonl')
        input_map={r.get('task_id'):r for r in inputs};a.check(len(input_map)==len(inputs),'unique_input_ids','Duplicate input task IDs.',role=role)
        role_ids[role]=set();dc=collections.Counter()
        for r in full:
            tid=r.get('task_id');domain=r.get('domain');ctx={'task_id':tid,'role':role,'domain':domain}
            if not isinstance(tid,str) or not tid:a.finding('task_id_schema','error','Task ID must be a nonempty string.',role=role);continue
            a.check(tid not in rows,'task_id_overlap','Task ID appears in more than one evaluator record.',**ctx);rows[tid]=(role,r);role_ids[role].add(tid);dc[domain]+=1;schema_keys.update(r.keys())
            a.check(set(r)==FULL_FIELDS,'full_record_schema','Unexpected or missing full-record fields.',actual_keys=sorted(r),**ctx)
            a.check(domain in EXPECTED_DOMAINS,'domain_schema','Unknown domain.',**ctx)
            for key in ['system_prompt','user_prompt','mcp_endpoint']:
                a.check(isinstance(r.get(key),str) and bool(r[key].strip()),'nonempty_text','Required string missing/empty.',field=key,**ctx)
            if isinstance(r.get('user_prompt'),str):prompt_buckets[hash_text(normalize_text(r['user_prompt']))].append(tid)
            a.check(type(r.get('number_of_runs')) is int and r['number_of_runs']>=1,'runs_schema','number_of_runs must be a positive integer.',**ctx)
            a.check(r.get('reset_database_between_runs') is True,'reset_required','Task does not require database reset.',**ctx)
            for key in ['selected_tools','restricted_tools']:
                v=r.get(key);ok=isinstance(v,list) and all(isinstance(x,str) and x.strip() and x==x.strip() for x in v)
                a.check(ok,'tools_schema','Tool list must contain nonempty trimmed strings.',field=key,**ctx)
                if ok:a.check(len(v)==len(set(v)),'duplicate_tool_names','Tool names repeat within a task list.',field=key,**ctx)
            selected=r.get('selected_tools') if isinstance(r.get('selected_tools'),list) else [];restricted=r.get('restricted_tools') if isinstance(r.get('restricted_tools'),list) else []
            a.check(bool(selected),'empty_selected_tools','No selected tools.',**ctx)
            if all(isinstance(x,str) for x in selected+restricted):
                a.check(not(set(selected)&set(restricted)),'selected_restricted_overlap','Tool both selected and restricted.',**ctx);tool_names.update(selected)
                for tool in selected:tool_signatures[tool].add(domain)
            ir=input_map.get(tid);a.check(ir is not None,'missing_input_record','Evaluator task lacks input record.',**ctx)
            if ir is not None:
                a.check(set(ir)==INPUT_FIELDS,'input_leakage_schema','Input record has extra/missing fields; verifiers/admin config must be excluded.',actual_keys=sorted(ir),**ctx)
                a.check(all(ir.get(k)==r.get(k) for k in INPUT_FIELDS),'input_evaluator_mismatch','Input fields differ from evaluator source.',**ctx)
            server_configs=r.get('gym_servers_config')
            if isinstance(server_configs,str):server_configs=a.decode(server_configs,tid+':gym_servers_config')
            a.check(isinstance(server_configs,list) and bool(server_configs),'gym_config_schema','Gym configs must be a nonempty list.',**ctx)
            if not isinstance(server_configs,list):server_configs=[]
            server_names=[]
            for i,g in enumerate(server_configs):
                if not isinstance(g,dict):a.finding('server_not_object','error','Server config is not an object.',index=i,**ctx);continue
                name=g.get('mcp_server_name');server_names.append(name)
                for key in ['mcp_server_name','mcp_server_url','seed_database_file']:
                    a.check(isinstance(g.get(key),str) and bool(g[key].strip()),'server_field_schema','Server field missing/empty.',field=key,server_index=i,**ctx)
                a.check(isinstance(g.get('context'),dict),'server_context_schema','Server context must be an object.',server_index=i,**ctx)
                url=g.get('mcp_server_url','');parsed=urlparse(url) if isinstance(url,str) else None
                a.check(bool(parsed and parsed.scheme in {'http','https'} and parsed.hostname),'server_url_schema','Malformed server URL.',server_index=i,**ctx)
            a.check(len(server_names)==len(set(server_names)),'duplicate_server_identity','Task has duplicate MCP server names.',**ctx)
            vs=r.get('verifiers')
            if isinstance(vs,str):vs=a.decode(vs,tid+':verifiers')
            a.check(isinstance(vs,list) and bool(vs),'empty_verifiers','Must not accept an empty verifier collection.',**ctx)
            if not isinstance(vs,list):vs=[]
            stats['verifiers']+=len(vs);by_name=collections.defaultdict(list);by_check=collections.defaultdict(list);by_query=collections.defaultdict(list);local=[]
            for i,v in enumerate(vs):
                vid=f'{tid}::v{i:04d}';vctx={**ctx,'verifier_index':i,'verifier_id':vid}
                if not isinstance(v,dict):a.finding('verifier_schema','error','Verifier is not an object.',**vctx);continue
                a.check(v.get('verifier_type')=='database_state','verifier_type','Unsupported verifier type.',**vctx)
                name=v.get('name');a.check(isinstance(name,str) and bool(name.strip()),'verifier_name','Verifier display name missing/empty.',**vctx)
                gym=v.get('gym_name');a.check(isinstance(gym,str) and gym in server_names,'verifier_gym_reference','Verifier gym does not match a task MCP server.',gym_name=gym,available_server_names=server_names,**vctx)
                cfg=v.get('validation_config');a.check(isinstance(cfg,dict),'validation_config_schema','Validation config must be an object.',**vctx)
                if not isinstance(cfg,dict):cfg={}
                query=cfg.get('query');valid_query=isinstance(query,str) and bool(query.strip());a.check(valid_query,'empty_sql_query','Verifier SQL query missing/empty.',**vctx)
                a.check('expected_value' in cfg,'missing_expected_value','Verifier expected value missing.',**vctx)
                cmp=cfg.get('comparison_type');comparison_types[str(cmp)]+=1;a.check(cmp in {'equals','greater_than','less_than','contains'},'comparison_type','Unsupported comparison operator.',**vctx)
                expected=cfg.get('expected_value');expected_types[type(expected).__name__]+=1
                if cmp in {'greater_than','less_than'}:a.check(isinstance(expected,(int,float,str)) and not isinstance(expected,bool),'ordered_comparison_type','Ordered comparison expected value must have an orderable scalar type; SQL result type still matters.',**vctx)
                if cmp=='contains':a.check(isinstance(expected,str),'contains_expected_type','contains comparator requires string expected value in upstream implementation.',**vctx)
                info,_=sql_info(query) if valid_query else ({'parse_status':'not_parsed_empty'},None);query_status[info['parse_status']]+=1
                if info.get('direct_scalar_count') and isinstance(expected,str):a.finding('count_expected_string','error','Direct scalar COUNT returns an integer, but expected_value is a string. Preserve the written numeric target/operator while normalizing representation; do not coerce unrelated text checks.',json_pointer=f'/verifiers/{i}/validation_config/expected_value',**vctx)
                if info['parse_status']=='parse_error':a.finding('sql_parser_error','warning','SQLite-dialect static parser rejected SQL; inspect parser compatibility and actual SQLite compilation before execution.',**vctx)
                if info.get('statement_count') is not None:a.check(info['statement_count']==1,'sql_statement_count','Verifier must have exactly one SQL statement.',statement_count=info['statement_count'],**vctx)
                if 'read_query_only' in info:a.check(info['read_query_only'],'sql_not_read_query','Verifier contains a non-query statement; do not execute automatically.',**vctx)
                qhash=info.get('canonical_sql_sha256') or (hash_text(query.strip()) if valid_query else None)
                check_key=canonical([gym,qhash,cmp,expected]);entry={'verifier_id':vid,'task_id':tid,'role':role,'domain':domain,'verifier_index':i,'display_name':name,'gym_name':gym,'comparison_type':cmp,'expected_value_type':type(expected).__name__,'expected_value_sha256':hash_text(canonical(expected)),'source_verifier_sha256':hash_text(canonical(v)),'query_sha256':hash_text(query) if valid_query else None,'normalized_check_sha256':hash_text(check_key),'sql_static':info,'duplicate_name_indices':[],'same_normalized_check_indices':[],'notes':['Metadata only; source expected values/SQL remain in evaluator_only records.']}
                local.append(entry);by_name[name].append(i);by_check[check_key].append(i);by_query[(gym,qhash)].append((i,cmp,expected,info.get('volatile_query',False)))
            index_entry={x['verifier_index']:x for x in local}
            for name,ix in by_name.items():
                if len(ix)>1:
                    stats['duplicate_name_groups']+=1;stats['verifiers_overwritten_if_keyed_by_name']+=len(ix)-1;name_affected.add(tid)
                    # A name-keyed dict retains only the final index of each name.
                    lost=[i for i in ix[:-1] if index_entry[i]['normalized_check_sha256']!=index_entry[ix[-1]]['normalized_check_sha256']]
                    if lost:name_loss_tasks.add(tid);stats['nonidentical_entries_overwritten_by_name']+=len(lost)
                    a.finding('duplicate_verifier_name','warning','Display-name keying loses required entries; evaluate every stable index. Some repeated checks may be equivalent.',indices=ix,nonidentical_lost_indices=lost,**ctx)
                    for i in ix:index_entry[i]['duplicate_name_indices']=ix
            for key,ix in by_check.items():
                if len(ix)>1:
                    duplicate_check_tasks.add(tid);stats['duplicate_normalized_check_groups']+=1;stats['redundant_normalized_check_entries']+=len(ix)-1
                    a.finding('duplicate_normalized_check','info','Same gym, normalized SQL, comparison and expected value repeats. Keep original indices; report duplicate-weighted diagnostic metric explicitly.',indices=ix,**ctx)
                    for i in ix:index_entry[i]['same_normalized_check_indices']=ix
            for key,entries in by_query.items():
                equal=[v for v in entries if v[1]=='equals']
                incompatible=[];seen_pairs=set()
                for i,cmp,e,vol in equal:
                    for k,cmp2,e2,vol2 in entries:
                        pair=tuple(sorted([i,k]))
                        if i==k or pair in seen_pairs:continue
                        seen_pairs.add(pair)
                        bad=False
                        if cmp2=='equals':bad=e!=e2
                        elif cmp2=='greater_than' and isinstance(e,(int,float)) and isinstance(e2,(int,float)):bad=not e>e2
                        elif cmp2=='less_than' and isinstance(e,(int,float)) and isinstance(e2,(int,float)):bad=not e<e2
                        elif cmp2=='contains' and isinstance(e2,str):bad=e2 not in str(e)
                        if bad:incompatible.append([i,k])
                if incompatible:
                    query_conflict_tasks.add(tid);stats['identical_query_constraint_conflicts']+=len(incompatible)
                    a.finding('identical_query_constraint_conflict','warning' if any(v[3] for v in entries) else 'error','Same normalized SQL and gym has incompatible result constraints. Requires curator decision; no replacement answer inferred.',index_pairs=incompatible,volatile_query=any(v[3] for v in entries),**ctx)
            surviving_checks={index_entry[ix[-1]]['normalized_check_sha256'] for ix in by_name.values()}
            all_checks={x['normalized_check_sha256'] for x in local}
            stats['distinct_normalized_checks_lost_by_name']+=len(all_checks-surviving_checks)
            a.inventory.extend(local)
        domain_counts[role]=dict(sorted(dc.items()))
        a.check(role_ids[role]==set(manifest.get('task_ids',{}).get(role,[])),'role_manifest_membership','Evaluator membership differs from manifest.',role=role)
        a.check(set(input_map)==role_ids[role],'input_manifest_membership','Input membership differs from evaluator membership.',role=role)
    active=set(rows);expected_total={'train':128,'development':41,'final_test':160}
    a.check({r:len(role_ids[r]) for r in ROLES}==expected_total,'role_quotas','Role totals must be128/41/160.')
    for d in EXPECTED_DOMAINS:
        expected={'train':24 if d in {'hr','itsm','csm','hybrid'} else 8,'development':20 if d=='itsm' else 3,'final_test':20}
        actual={r:domain_counts[r].get(d,0) for r in ROLES};a.check(actual==expected,'domain_quotas','Domain quotas changed.',domain=d,actual=actual,expected=expected)
    excluded=set(manifest.get('excluded_reserve_ids',[]));held=set(manifest.get('quarantined_ids',[]))
    a.check(len(active)==329 and len(excluded)==311 and len(held)==9 and not(active&excluded or active&held or excluded&held) and len(active|excluded|held)==649,'source_partition','Active/excluded/held partition must be329+311+9=649 without overlap.')
    active_group_map={};group_coverage=set()
    for group in groups.get('groups',[]):
        ids=group.get('active_task_ids',[]);roles_in={rows[t][0] for t in ids if t in rows}
        a.check(set(ids)<=active and len(roles_in)==1 and roles_in=={group.get('active_role')},'workflow_group_isolation','Audited workflow group crosses roles or has invalid membership.',group_id=group.get('group_id'))
        a.check(not(group_coverage&set(ids)),'workflow_group_duplicate_membership','Task appears in multiple group records.',group_id=group.get('group_id'));group_coverage.update(ids)
        members=sorted(ids+group.get('excluded_related_ids',[]));derived='family-'+hash_text('\n'.join(members))[:16]
        a.check(derived==group.get('group_id') and len(members)==group.get('source_group_size'),'workflow_group_hash','Group source-member hash/size mismatch.',group_id=group.get('group_id'))
        for t in ids:active_group_map[t]=group.get('group_id')
    a.check(group_coverage==active,'workflow_group_coverage','Workflow metadata does not cover every active task.')
    duplicate_prompts=[]
    for ph,tids in prompt_buckets.items():
        if len(tids)>1:
            same_roles={rows[t][0] for t in tids};duplicate_prompts.append({'task_ids':tids,'roles':sorted(same_roles),'normalized_user_sha256':ph})
            a.finding('duplicate_user_prompt','error' if len(same_roles)>1 else 'info','Identical normalized user prompts repeat; cross-role copies would be leakage.',task_ids=tids,roles=sorted(same_roles))
    # Independently inspect all source family edges when portable audit inputs exist.
    audit_paths=list(args.family_audit)
    if not audit_paths:
        for name in manifest.get('selection',{}).get('source_family_audits',{}):
            options=[modal_root/'data/metadata'/name,modal_root/'data/metadata/family_audits'/name,project_root/'work'/name]
            found=next((p for p in options if p.is_file()),None)
            if found:audit_paths.append(found)
    family_checks=[]
    for p in audit_paths:
        obj=a.readj(p) or {};expected=manifest.get('selection',{}).get('source_family_audits',{}).get(p.name)
        if expected:a.check(sha_file(p)==expected,'source_family_audit_hash','Family audit source differs from frozen allocation input.',file=p.name)
        buckets=collections.defaultdict(list)
        for tid,gid in obj.get('task_to_group',{}).items():buckets[gid].append(tid)
        for gid,tids in buckets.items():a.check(len({rows[t][0] for t in tids if t in rows})<=1,'source_family_group_isolation','Source family crosses active roles.',source=p.name,source_group=gid)
        count=0
        for e in obj.get('edges',[])+obj.get('cross_domain_links',[]):
            if not isinstance(e,dict):continue
            x=e.get('a',e.get('task_a'));y=e.get('b',e.get('task_b'))
            if x and y:
                count+=1
                if x in rows and y in rows:a.check(rows[x][0]==rows[y][0],'source_family_edge_isolation','Source family edge crosses active roles.',source=p.name,task_a=x,task_b=y)
        family_checks.append({'file':p.name,'sha256':sha_file(p),'groups_checked':len(buckets),'edges_checked':count})
    normalization_replay={'performed':False}
    replay_changes=collections.defaultdict(list)
    if payload!=base:
        normalization_path=payload/'metadata/normalization_manifest.json'
        ledger_path=payload/'metadata/normalization_changes.jsonl'
        nm=a.readj(normalization_path) or {};ledger=a.readjl(ledger_path)
        a.check(nm.get('source_release_sha256')==sha_file(base/'split_manifest.json'),'normalization_source_hash','Normalization ledger references another source manifest.')
        a.check(ledger_path.is_file() and nm.get('changes_file_sha256')==sha_file(ledger_path),'normalization_ledger_hash','Normalization change ledger hash mismatch.')
        for relative,expected in nm.get('working_file_sha256',{}).items():
            wp=payload.parent/relative
            a.check(wp.is_file() and sha_file(wp)==expected,'normalized_working_file_hash','Working file differs from normalization manifest.',file=relative)
        cleaner=modal_root/'scripts/clean_dataset.py'
        if cleaner.is_file():a.check(sha_file(cleaner)==nm.get('cleaner_sha256'),'normalizer_source_hash','Cleaner code differs from the recorded version.')
        observed=collections.Counter(c.get('kind') for c in ledger)
        a.check(dict(observed)==nm.get('change_counts'),'normalization_change_counts','Normalization kind counts differ from manifest.')
        seen=set()
        for change in ledger:
            key=(change.get('role'),change.get('task_id'),change.get('path'))
            a.check(key not in seen,'duplicate_normalization_path','Field changed more than once in normalization ledger.',task_id=change.get('task_id'),path=change.get('path'));seen.add(key)
            a.check(change.get('task_id') in rows and rows[change['task_id']][0]==change.get('role'),'normalization_task_membership','Normalization ledger task/role invalid.',task_id=change.get('task_id'))
            replay_changes[(change.get('role'),change.get('task_id'))].append(change)
        normalization_replay={'performed':True,'changes':len(ledger),'by_kind':dict(observed),'ledger_sha256':sha_file(ledger_path),'no_sql_or_comparator_changes_permitted':True}
    # Enumerate only narrow, source-derived representation normalizations. Never apply them here.
    normalization_candidates=[];working_difference_count=0
    for role in ROLES:
        for source in a.readjl(base/'evaluator_only'/f'{role}.jsonl'):
            tid=source['task_id'];expected_working=copy.deepcopy(source);selected=source.get('selected_tools',[])
            if isinstance(selected,list) and all(isinstance(t,str) for t in selected):
                dedup=list(dict.fromkeys(selected))
                if dedup!=selected:
                    normalization_candidates.append({'task_id':tid,'role':role,'domain':source['domain'],'json_pointer':'/selected_tools','old_value':selected,'new_value':dedup,'operation':'order_preserving_deduplication','apply_to':['task_inputs','evaluator_only'],'reason':'Remove repeated function identity entries without changing available tool set or first-occurrence order.'})
                    expected_working['selected_tools']=dedup
            for i,v in enumerate(source.get('verifiers',[])):
                c=v.get('validation_config',{});ev=c.get('expected_value');q=c.get('query')
                si,_=sql_info(q) if isinstance(q,str) else ({},None)
                if si.get('direct_scalar_count') and isinstance(ev,str) and re.fullmatch(r'[+-]?\d+',ev.strip()):
                    number=int(ev.strip())
                    normalization_candidates.append({'task_id':tid,'role':role,'domain':source['domain'],'json_pointer':f'/verifiers/{i}/validation_config/expected_value','verifier_index':i,'old_value':ev,'new_value':number,'operation':'count_integer_representation','apply_to':['evaluator_only'],'comparison_type_unchanged':c.get('comparison_type'),'query_sha256_unchanged':hash_text(q),'reason':'SQLite direct scalar COUNT is integer-valued. Convert numeric target representation only; keep query, comparator, threshold magnitude, membership and other fields unchanged. This does not certify semantic task alignment.'})
                    expected_working['verifiers'][i]['validation_config']['expected_value']=number
            if payload!=base and tid in rows:
                replay=copy.deepcopy(source)
                for change in replay_changes[(role,tid)]:
                    path=change.get('path','');kind=change.get('kind');before=change.get('before');after=change.get('after');valid=False;container=None;field=None
                    if kind=='deduplicate_tool_names_preserving_order' and path in {'selected_tools','restricted_tools'}:
                        container=replay;field=path
                        valid=isinstance(before,list) and all(isinstance(t,str) for t in before) and after==list(dict.fromkeys(before))
                    elif kind=='unique_verifier_identity':
                        match=re.fullmatch(r'verifiers\[(\d+)\]\.name',path)
                        if match and int(match[1])<len(replay['verifiers']):
                            ix=int(match[1]);container=replay['verifiers'][ix];field='name'
                            valid=after==f'check-{ix:04d}: {before}'
                    elif kind=='direct_count_numeric_type_only':
                        match=re.fullmatch(r'verifiers\[(\d+)\]\.validation_config\.expected_value',path)
                        if match and int(match[1])<len(replay['verifiers']):
                            ix=int(match[1]);container=replay['verifiers'][ix]['validation_config'];field='expected_value';si,_=sql_info(container.get('query',''))
                            valid=si.get('direct_scalar_count',False) and isinstance(before,str) and re.fullmatch(r'[+-]?\d+',before.strip()) is not None and type(after) is int and after==int(before.strip()) and container.get('comparison_type') in {'equals','greater_than','less_than'}
                    a.check(bool(valid and container is not None and canonical(container.get(field))==canonical(before)),'normalization_rule_and_preimage','Ledger transformation is outside the narrow allowed rules or its before value does not match immutable source.',task_id=tid,path=path,kind=kind)
                    if valid and container is not None:container[field]=after
                actual=rows[tid][1]
                if canonical(actual)!=canonical(source):working_difference_count+=1
                a.check(canonical(actual)==canonical(replay),'working_normalization_replay','Working evaluator record is not exact replay of the verified normalization ledger.',task_id=tid,role=role)
                # Source-derived count and tool corrections must all have been applied.
                for i,v in enumerate(actual.get('verifiers',[])):
                    a.check(v.get('name')==f'check-{i:04d}: {source["verifiers"][i]["name"]}','indexed_verifier_name_contract','Working verifier identity does not preserve its original label under a unique index.',task_id=tid,verifier_index=i)
    semantic_flags=[{'task_id':'task_20260115_154856_907_1628b966_275e920f','role':'final_test','domain':'hybrid','status':'UNRESOLVED_CURATOR_REVIEW','verifier_indices':[0,1,2],'type':'goal_coverage_and_threshold_alignment','finding':'Source task requests an open-case overview, a specific case closure/reassignment, and spreadsheet content/name/description. Current checks cover active account count, remaining open-case count greater than1, and spreadsheet name/MIME only. They do not verify the requested case mutation or spreadsheet fields/content/description. The remaining-case threshold is not established by the user request and disagrees with the verifier description at least one.','allowed_representation_fix':'Convert COUNT targets from strings to integers while preserving all existing numeric values and comparison operators.','not_authorized_as_automatic_fix':'Do not lower the threshold, add/remove verifiers, infer replacement SQL, drop the task or change its frozen split.','effect':'Do not claim complete semantic cleanliness or strict user-goal success from this task until separately reviewed against the environment.'}]
    for flag in semantic_flags:a.finding('semantic_verifier_alignment_unresolved','warning',flag['finding'],task_id=flag['task_id'],role=flag['role'],domain=flag['domain'])
    old_itsm_status='not_rechecked_old_path_not_portable'
    stats.update({'tasks':len(rows),'tasks_with_duplicate_names':len(name_affected),'tasks_losing_nonidentical_named_checks':len(name_loss_tasks),'tasks_with_redundant_normalized_checks':len(duplicate_check_tasks),'tasks_with_identical_query_conflicts':len(query_conflict_tasks),'distinct_selected_tool_names':len(tool_names),'input_fields_per_record':6})
    errors=[f for f in a.findings if f['severity']=='error'];warnings=[f for f in a.findings if f['severity']=='warning']
    result={'audit_version':'static-source-audit-v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'dataset_path':str(base),'payload_root':str(payload),'working_payloads_audited':payload!=base,'dataset_manifest_sha256':sha_file(base/'split_manifest.json'),'source_immutable':True,'source_audit_report':'dataset_source_audit.json' if payload!=base else None,'status':'STRUCTURAL_ERRORS_REVIEW_REQUIRED' if errors else 'STATIC_CHECKS_PASS_WITH_QUALITY_CAVEATS','readiness':{'task_specifications_present':len(rows)==329,'sft_demonstrations_ready':False,'sql_runtime_validated':False,'tool_backend_validated':False,'semantic_task_feasibility_validated':False,'safe_to_claim_all_tasks_clean':False,'paid_execution_performed':False},'dependencies':{'python':sys.version.split()[0],'optional_sqlglot_version':getattr(sqlglot,'__version__',None),'sql_dialect':'sqlite','sql_execution_performed':False},'counts':dict(stats),'role_counts':{r:len(role_ids[r]) for r in ROLES},'domain_counts_by_role':domain_counts,'comparison_types':dict(comparison_types),'expected_value_types':dict(expected_types),'sql_parse_counts':dict(query_status),'source_hash_checks':source_hashes,'source_family_checks':family_checks,'old_itsm_preservation':'Prior independent release audit verified24train subset54,20development,20finaltest,and9holds unchanged; this portable script checks immutable release hashes rather than reading external old holdout files.','duplicate_normalized_user_prompt_sets':duplicate_prompts,'tool_identity_scope':{'string_lists_and_unique_names_checked':True,'selected_restricted_disjoint_checked':True,'live_mcp_catalog_match_checked':False,'schema_argument_validity_checked':False,'note':'Tool names alone cannot prove server implementation exists or arguments behave correctly.'},'check_invocation_counts':dict(a.checks),'normalization_replay':normalization_replay,'normalization_candidates':normalization_candidates,'working_modified_record_count':working_difference_count,'normalization_scope':'Exact listed source-derived transforms only; source records and frozen memberships are immutable.','semantic_quality_flags':semantic_flags,'findings_by_code':dict(collections.Counter(f['code'] for f in a.findings)),'error_count':len(errors),'warning_count':len(warnings),'findings':a.findings,'limits':['SQL parsing does not establish table/column existence, SQLite/server feature support, SQL result shape, expected result correctness, or human-task/verifier alignment.','Normalized SQL equality identifies duplicate forms only; no complete semantic-equivalence proof is attempted.','Family review is bounded and nonexhaustive. Shared system policies and synthetic databases remain.','Curator review of protected tasks was authorized for this audit; do not provide this report or evaluator metadata as agent observations, training demonstrations, or adaptive final-test feedback.','Task specifications are not successful teacher trajectories and cannot directly train the adapter.']}
    args.report_dir.mkdir(parents=True,exist_ok=True);args.inventory.parent.mkdir(parents=True,exist_ok=True)
    (args.report_dir/'dataset_audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    with args.inventory.open('w') as f:
        for entry in a.inventory:f.write(json.dumps(entry,ensure_ascii=False)+'\n')
    md=['# Static audit of the329task release','',f'Status: **{result["status"]}**. Audited329 task specifications; no API/GPU/Docker/model runs or SQL execution. Sources and membership were not changed.','',f'- Roles: {result["role_counts"]}.',f'- Verifier entries: {stats["verifiers"]}; distinct selected tool names: {len(tool_names)}.',f'- SQL parser: sqlglot {getattr(sqlglot,"__version__","not installed")}, SQLite dialect; results: {dict(query_status)}.',f'- Structural/error findings: {len(errors)}; warning occurrences: {len(warnings)}.','', '## Actionable findings','', '| Finding | Count | Required action |','|---|---:|---|',f'| Tasks with repeated verifier names |{len(name_affected)}|Evaluate by task ID + stable zero-based verifier index, never a name-keyed dictionary.|',f'| Entries overwritten by name-keying |{stats["verifiers_overwritten_if_keyed_by_name"]}|Retain every original verifier entry; this loses {stats["distinct_normalized_checks_lost_by_name"]} distinct normalized checks.|',f'| Tasks losing nonidentical named checks |{len(name_loss_tasks)}|Treat this as a scoring correctness issue, not cosmetic duplication.|',f'| Redundant normalized-check entries |{stats["redundant_normalized_check_entries"]}|Keep immutable checks; disclose duplicate weighting in diagnostic verifier rates.|',f'| Tasks with incompatible same-query constraints |{len(query_conflict_tasks)}|Curator review is required before a claim that these tasks can pass. No replacement targets inferred.|',f'| SQL parser failures |{query_status["parse_error"]}|Check actual SQLite compilation and intended schema; parser rejection alone is not proof of a server bug.|','', '## Concrete errors and review warnings','',f'Frozen-source normalization candidates: {len(normalization_candidates)} exact field edits, enumerated with original/replacement values in the curator-only JSON report. They are not applied by this script.']
    for f in a.findings:
        if f['severity']=='error' or f['code'] in {'sql_parser_error','identical_query_constraint_conflict','verifier_gym_reference','semantic_verifier_alignment_unresolved'}:
            ident=f.get('verifier_id',f.get('task_id',f.get('file',f.get('group_id','release'))));md.append(f'- `{f["code"]}` — `{ident}`: {f["message"]}')
    if not errors and not query_status['parse_error']:md.append('No malformed required fields, empty queries, broken gym references, invalid role quotas, or detected cross-role audited-family leakage were found.')
    md+=['','## What remains unverified','','The329 tasks are structurally present. This audit cannot certify that all are semantically clean or executable. Live tool catalogs, per-task reset/isolation, SQL schema/result shape, task/verifier agreement, and final-state completeness still require controlled environment validation. No successful SFT demonstrations have been created.','', 'The curator-only verifier inventory assigns stable IDs and records hashes, parser results, table names, and duplicate relationships. It deliberately omits source SQL text and expected values. Do not pass inventory or evaluator-only files to the agent.','', '## Reproduce','', '```bash','python3 MODAL/scripts/audit_dataset.py','```','', 'For normalized working files, add `--payload-root MODAL/data`. The script validates every recorded mechanical transformation and unchanged full records against the immutable source.', '', 'Optional SQL parsing dependency: `sqlglot==30.6.0`. Without it, the script explicitly reports SQL parsing unverified. All other checks use the standard library.','', 'Detailed findings and task/verifier identifiers are in `dataset_audit.json`; no record corrections were applied.']
    (args.report_dir/'dataset_audit.md').write_text('\n'.join(md)+'\n')
    print(json.dumps({'status':result['status'],'counts':dict(stats),'sql_parse_counts':dict(query_status),'findings_by_code':result['findings_by_code'],'errors':len(errors),'warnings':len(warnings)},indent=2))
    return 1 if errors else 0
if __name__=='__main__':raise SystemExit(main())

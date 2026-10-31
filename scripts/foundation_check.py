#!/usr/bin/env python3
"""One-command, local-only foundation audit.

No network, cloud, Docker, model/tokenizer download, training, or spending calls.
Final-test records are used only for opaque integrity replay and metadata checks;
the checker does not review question text, interpret verifier SQL, or score tasks.
Exit0: local SFT artifacts are validated; runtime/cloud readiness is separate.
Exit2: missing/not-ready SFT artifacts.
Exit1: an integrity check failed. Only reports/foundation_audit.{json,md} are written.
"""
from __future__ import annotations
import argparse, collections, copy, datetime, hashlib, importlib.util, json, os, re, sys, zipfile
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLES = ('train', 'development', 'final_test')
EXPECTED = {'train':128, 'development':41, 'final_test':160}
INPUT_FIELDS = ('task_id','domain','system_prompt','user_prompt','selected_tools','restricted_tools')
EXCLUDED_NAMES = {'.git','__pycache__','.venv','.venv-prepare','.venv-audit','node_modules'}
sys.dont_write_bytecode = True


def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)

def object_hash(x):return hashlib.sha256(canonical(x).encode()).hexdigest()

def file_hash(path):
    digest=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):digest.update(block)
    return digest.hexdigest()

def local_path(path):
    p=Path(path)
    if not p.is_absolute():p=ROOT/p
    resolved=p.resolve()
    if not resolved.is_relative_to(ROOT):raise ValueError(f'Path leaves this workspace: {p}')
    return resolved

def rel(path):return str(Path(path).relative_to(ROOT))

class Check:
    def __init__(self):self.errors=[];self.notes=[];self.checks=collections.Counter()
    def require(self,ok,code,detail,**context):
        self.checks[code]+=1
        if not ok:self.errors.append({'code':code,'detail':detail,**context})
        return bool(ok)
    def load(self,path,required=True):
        p=local_path(path)
        if not p.is_file():
            if required:self.errors.append({'code':'missing_required_file','path':rel(p)})
            return None
        try:return json.loads(p.read_text())
        except (ValueError,OSError) as e:
            self.errors.append({'code':'invalid_json','path':rel(p),'error':type(e).__name__});return None
    def jsonl(self,path,required=True):
        p=local_path(path)
        if not p.is_file():
            if required:self.errors.append({'code':'missing_required_jsonl','path':rel(p)})
            return []
        out=[]
        try:
            with p.open() as f:
                for n,line in enumerate(f,1):
                    if line.strip():
                        record=json.loads(line)
                        if not isinstance(record,dict):raise ValueError('record not object')
                        out.append(record)
        except (ValueError,OSError) as e:self.errors.append({'code':'invalid_jsonl','path':rel(p),'line':n,'error':type(e).__name__})
        return out
    def check_hash(self,path,expected,code='file_hash'):
        p=local_path(path)
        return self.require(p.is_file() and file_hash(p)==expected,code,'Missing file or hash mismatch.',path=rel(p))


def import_local(path,name):
    path=local_path(path)
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod
    spec.loader.exec_module(mod)
    return mod


def bounded_file_inventory():
    result=[];external_symlinks=[]
    for folder,dirs,files in os.walk(ROOT,followlinks=False):
        dirs[:]=[d for d in dirs if d not in EXCLUDED_NAMES and not d.startswith('.venv')]
        for name in files:
            p=Path(folder)/name
            if not p.resolve().is_relative_to(ROOT):external_symlinks.append(rel(p));continue
            result.append(p)
    return result,external_symlinks


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',action='store_true',help='Print the full JSON report instead of the short summary.')
    args=parser.parse_args();c=Check()
    source=ROOT/'data/source_release';working=ROOT/'data';metadata=working/'metadata'
    manifest=c.load(source/'split_manifest.json') or {}
    same_manifest=c.load(metadata/'split_manifest.json') or {}
    c.require(canonical(manifest)==canonical(same_manifest),'frozen_manifest_copy','Working metadata is not the frozen source manifest.')
    source_checks=c.load(source/'checksums.json') or {}
    for path,expected in source_checks.items():c.check_hash(source/path,expected,'immutable_release_hash')
    for path,expected in manifest.get('export_sha256',{}).items():c.check_hash(source/path,expected,'immutable_payload_hash')
    roles={};source_records={};working_records={};domain_counts={};required_seeds=set();required_training_seeds=set();required_servers=set();selected_tools=set()
    copy_counts={};active=set()
    for role in ROLES:
        expected_ids=manifest.get('task_ids',{}).get(role,[])
        c.require(len(expected_ids)==EXPECTED[role] and len(set(expected_ids))==EXPECTED[role],'frozen_role_quota','Frozen role quota/unique IDs differ.',role=role)
        sd=c.jsonl(source/'evaluator_only'/f'{role}.jsonl');si=c.jsonl(source/'task_inputs'/f'{role}.jsonl')
        wd=c.jsonl(working/'evaluator_only'/f'{role}.jsonl');wi=c.jsonl(working/'task_inputs'/f'{role}.jsonl')
        copies={'source_evaluator':sd,'source_inputs':si,'working_evaluator':wd,'working_inputs':wi}
        copy_counts[role]={k:len(v) for k,v in copies.items()}
        for name,rs in copies.items():
            ids=[r.get('task_id') for r in rs]
            c.require(len(ids)==len(set(ids)) and set(ids)==set(expected_ids),'copy_id_membership','Copy membership differs from frozen IDs.',role=role,copy=name)
        sm={r['task_id']:r for r in sd};wm={r['task_id']:r for r in wd};sim={r['task_id']:r for r in si};wim={r['task_id']:r for r in wi}
        source_records.update(sm);working_records.update(wm)
        dc=collections.Counter()
        for tid in expected_ids:
            c.require(tid not in active,'split_overlap','Task appears in multiple active roles.',task_id=tid);active.add(tid);roles[tid]=role
            if tid not in sm or tid not in wm:continue
            for name,full,inp in [('source',sm[tid],sim.get(tid)),('working',wm[tid],wim.get(tid))]:
                expected_input={key:full.get(key) for key in INPUT_FIELDS}
                c.require(isinstance(inp,dict) and canonical(inp)==canonical(expected_input),'input_projection','Input contains missing/extra/different fields relative to the model-visible projection.',task_id=tid,copy=name)
            row=wm[tid];dc[row.get('domain')]+=1
            selected_tools.update(t for t in row.get('selected_tools',[]) if isinstance(t,str))
            config=row.get('gym_servers_config',[])
            if isinstance(config,str):config=json.loads(config)
            for server in config:
                if isinstance(server,dict):
                    if isinstance(server.get('seed_database_file'),str):
                        seed=server['seed_database_file'].replace('\\','/');required_seeds.add(seed)
                        if role=='train':required_training_seeds.add(seed)
                    if isinstance(server.get('mcp_server_name'),str):required_servers.add(server['mcp_server_name'])
        domain_counts[role]=dict(sorted(dc.items()))
    c.require(len(active)==329,'selected_unique_count','Need exactly329 selected identities, not counts of copies.')
    excluded=set(manifest.get('excluded_reserve_ids',[]));quarantined=set(manifest.get('quarantined_ids',[]))
    c.require(len(excluded)==311 and len(quarantined)==9 and not(active&excluded or active&quarantined or excluded&quarantined) and len(active|excluded|quarantined)==649,'exclusion_partition','329 active +311 excluded +9 prior holds must partition649.')
    for domain in ['calendar','csm','drive','email','hr','hybrid','itsm','teams']:
        expected={'train':24 if domain in {'csm','hr','itsm','hybrid'} else 8,'development':20 if domain=='itsm' else 3,'final_test':20}
        actual={r:domain_counts[r].get(domain,0) for r in ROLES}
        c.require(actual==expected,'domain_quotas','Domain allocation changed.',domain=domain)

    # Replay exact normalization metadata without interpreting question or SQL text.
    nm=c.load(metadata/'normalization_manifest.json') or {};changes=c.jsonl(metadata/'normalization_changes.jsonl')
    c.check_hash(source/'split_manifest.json',nm.get('source_release_sha256'),'normalization_source_hash')
    c.check_hash(metadata/'normalization_changes.jsonl',nm.get('changes_file_sha256'),'normalization_ledger_hash')
    if nm.get('cleaner_sha256'):c.check_hash(ROOT/'scripts/clean_dataset.py',nm['cleaner_sha256'],'normalizer_code_hash')
    for path,expected in nm.get('working_file_sha256',{}).items():c.check_hash(ROOT/path,expected,'normalized_payload_hash')
    changes_by_kind=collections.Counter(x.get('kind') for x in changes)
    c.require(dict(changes_by_kind)==nm.get('change_counts'),'normalization_counts','Ledger transformation counts differ from recorded manifest.')
    reconstructed=copy.deepcopy(source_records);seen_changes=set()
    for change in changes:
        tid=change.get('task_id');path=change.get('path','');kind=change.get('kind');before=change.get('before');after=change.get('after')
        c.require(tid in reconstructed and roles.get(tid)==change.get('role'),'normalization_membership','Normalization entry has unknown task or wrong role.',task_id=tid)
        c.require((tid,path) not in seen_changes,'normalization_unique_field','Normalization field repeated.',task_id=tid,path=path);seen_changes.add((tid,path))
        if tid not in reconstructed:continue
        row=reconstructed[tid];container=None;field=None;valid=False
        if kind=='deduplicate_tool_names_preserving_order' and path in {'selected_tools','restricted_tools'}:
            container=row;field=path;valid=isinstance(before,list) and all(isinstance(x,str) for x in before) and after==list(dict.fromkeys(before))
        elif kind=='unique_verifier_identity':
            match=re.fullmatch(r'verifiers\[(\d+)\]\.name',path)
            if match and int(match[1])<len(row.get('verifiers',[])):
                ix=int(match[1]);container=row['verifiers'][ix];field='name';valid=after==f'check-{ix:04d}: {before}'
        elif kind=='direct_count_numeric_type_only':
            match=re.fullmatch(r'verifiers\[(\d+)\]\.validation_config\.expected_value',path)
            if match and int(match[1])<len(row.get('verifiers',[])):
                container=row['verifiers'][int(match[1])]['validation_config'];field='expected_value'
                valid=isinstance(before,str) and re.fullmatch(r'[+-]?\d+',before.strip()) is not None and type(after) is int and after==int(before.strip())
        c.require(bool(valid and container is not None and canonical(container.get(field))==canonical(before)),'normalization_replay_rule','Transformation is outside recorded representation rules or preimage mismatches.',task_id=tid,path=path)
        if valid and container is not None:container[field]=after
    for tid,row in reconstructed.items():
        c.require(tid in working_records and canonical(working_records[tid])==canonical(row),'exact_normalization_replay','Working full record differs from exact normalization replay.',task_id=tid)

    groups=c.load(metadata/'workflow_groups.json') or {};group_coverage=set();group_roles={};group_count=0
    for group in groups.get('groups',[]):
        ids=group.get('active_task_ids',[]);rset={roles[t] for t in ids if t in roles};all_members=sorted(ids+group.get('excluded_related_ids',[]))
        c.require(set(ids)<=active and len(rset)==1 and rset=={group.get('active_role')},'family_isolation','Audited group crosses active roles.',group_id=group.get('group_id'))
        c.require(not(group_coverage&set(ids)),'group_duplicate_membership','Task appears in multiple group rows.',group_id=group.get('group_id'));group_coverage.update(ids)
        c.require('family-'+hashlib.sha256('\n'.join(all_members).encode()).hexdigest()[:16]==group.get('group_id') and len(all_members)==group.get('source_group_size'),'group_member_hash','Group-member hash or source count differs.',group_id=group.get('group_id'))
        group_count+=1
        for tid in ids:group_roles[tid]=group.get('group_id')
    c.require(group_coverage==active,'group_coverage','Audited group records do not cover all selected tasks.')
    source_family_audits=[]
    for name,expected_hash in manifest.get('selection',{}).get('source_family_audits',{}).items():
        path=metadata/name
        if not c.check_hash(path,expected_hash,'family_audit_hash'):continue
        audit=c.load(path) or {};buckets=collections.defaultdict(list)
        for tid,gid in audit.get('task_to_group',{}).items():buckets[gid].append(tid)
        for gid,ids in buckets.items():c.require(len({roles[t] for t in ids if t in roles})<=1,'source_family_isolation','Source group crosses active roles.',group_id=str(gid))
        edge_count=0
        for edge in audit.get('edges',[])+audit.get('cross_domain_links',[]):
            if not isinstance(edge,dict):continue
            x=edge.get('a',edge.get('task_a'));y=edge.get('b',edge.get('task_b'))
            if x and y:
                edge_count+=1
                if x in roles and y in roles:c.require(roles[x]==roles[y],'source_family_edge','Audited edge crosses active roles.',task_a=x,task_b=y)
        source_family_audits.append({'file':rel(path),'groups':len(buckets),'edges':edge_count,'sha256':file_hash(path)})

    config=c.load(ROOT/'config/training.json') or {};trace_schema=c.load(ROOT/'config/trace_schema.json') or {};receipt_schema=c.load(ROOT/'config/verifier_receipt.schema.json') or {}
    c.require(config.get('expected_training_tasks')==128 and config.get('max_seq_length')==16384,'training_recipe','Initial recipe must preserve128 training IDs and16K max sequence.')
    c.check_hash(metadata/'split_manifest.json',config.get('split_manifest_sha256'),'training_split_binding')
    model_revision=config.get('model_revision');c.require(isinstance(model_revision,str) and re.fullmatch(r'[0-9a-f]{40}',model_revision) is not None,'immutable_model_revision','Model revision must be immutable.')
    required_trace={'source_task_id','messages','tools','review','provenance'};required_receipt={'schema_version','source_task_id','status','checks_total','checks_passed','model_visible_sha256','task_input_sha256','verifier_contract_sha256','verifier_revision','outcomes'}
    c.require(required_trace<=set(trace_schema.get('required',[])),'trace_schema_contract','Trajectory schema misses required provenance fields.')
    c.require(required_receipt<=set(receipt_schema.get('required',[])) and receipt_schema.get('properties',{}).get('schema_version',{}).get('const')==2,'receipt_schema_contract','Receipt schema must require version2, public-input hash and per-index outcomes, not aggregate counts alone.')
    outcome_schema=receipt_schema.get('properties',{}).get('outcomes',{}).get('items',{})
    c.require({'verifier_index','verifier_name','passed'}<=set(outcome_schema.get('required',[])),'receipt_outcome_schema','Per-check receipt outcomes lack index/name/pass binding.')
    template=ROOT/'config/qwen3_5_think_training.jinja';tokenizer_report=c.load(ROOT/'reports/data_checkpoint_validation.json',required=False) or {}
    historical_tokenizer=tokenizer_report.get('real_tokenizer_smoke',{})
    template_expected=tokenizer_report.get('template',{}).get('sha256')
    c.check_hash(template,template_expected,'training_template_hash')

    collection_root=ROOT/'data/collection';collection_manifest=c.load(collection_root/'collection_manifest.json',required=False) or {}
    queue=c.jsonl(collection_root/'task_index.jsonl',required=False);requirements=c.jsonl(collection_root/'evaluator_receipt_requirements.jsonl',required=False)
    collection={'manifest_present':bool(collection_manifest),'queue_rows':len(queue),'requirement_rows':len(requirements),'verified_demonstrations_from_queue':0,'status_counts':dict(collections.Counter(r.get('status') for r in queue)),'actual_trace_or_receipt_content_generated_by_checker':False}
    train_ids_for_queue=set(manifest.get('task_ids',{}).get('train',[]))
    if collection_manifest:
        for name,expected in collection_manifest.get('artifact_sha256',{}).items():c.check_hash(collection_root/name,expected,'collection_artifact_hash')
        for name,expected in collection_manifest.get('source_file_sha256',{}).items():c.check_hash(ROOT/name,expected,'collection_source_hash')
        c.check_hash(ROOT/'scripts/build_collection_queue.py',collection_manifest.get('builder_sha256'),'collection_builder_hash')
        c.require({r.get('task_id') for r in queue}==train_ids_for_queue and len(queue)==128,'collection_training_membership','Collection queue must contain exactly128 frozen training IDs, never held-out IDs.')
        c.require({r.get('task_id') for r in requirements}==train_ids_for_queue and len(requirements)==128,'receipt_requirements_membership','Receipt requirements must cover exactly128 frozen training IDs.')
        c.require({r.get('queue_order') for r in queue}==set(range(1,129)),'collection_queue_order','Queue ordering must cover1 through128 exactly.')
        train_inputs=c.jsonl(ROOT/'data/task_inputs/train.jsonl');train_input_map={r['task_id']:(n,r) for n,r in enumerate(train_inputs,1)}
        train_contracts=c.jsonl(ROOT/'data/evaluator_only/train.jsonl');train_contract_map={r['task_id']:(n,r) for n,r in enumerate(train_contracts,1)}
        req_map={r.get('task_id'):r for r in requirements};total_checks=0
        for item in queue:
            tid=item.get('task_id')
            if tid not in train_input_map or tid not in train_contract_map:continue
            iline,inp=train_input_map[tid];eline,evaluator=train_contract_map[tid];need=req_map.get(tid,{})
            c.require(item.get('role')=='train' and item.get('domain')==inp['domain'],'queue_role_domain','Collection role/domain mismatch.',task_id=tid)
            c.require(item.get('input_sha256')==object_hash(inp) and need.get('input_sha256')==object_hash(inp),'queue_input_binding','Queue/requirements do not bind exact normalized training input.',task_id=tid)
            c.require(item.get('source_input_file')=='data/task_inputs/train.jsonl' and item.get('source_input_line')==iline,'queue_source_locator','Queue source file/line locator mismatch.',task_id=tid)
            c.require(item.get('required_tool_names')==inp.get('selected_tools'),'queue_tool_allowlist','Queue tools differ from training input allowlist.',task_id=tid)
            c.require(item.get('workflow_group_id')==group_roles.get(tid),'queue_workflow_group','Queue family ID differs from frozen group metadata.',task_id=tid)
            expected_count=len(evaluator.get('verifiers',[]));total_checks+=expected_count
            c.require(need.get('role')=='train' and need.get('contract_source_file')=='data/evaluator_only/train.jsonl' and need.get('contract_source_line')==eline,'requirements_contract_locator','Requirement contract locator mismatch.',task_id=tid)
            c.require(need.get('required_checks_total')==expected_count and need.get('required_verifier_indices')==list(range(expected_count)) and need.get('verifier_contract_sha256')==object_hash(evaluator['verifiers']),'requirements_full_contract_binding','Receipt requirement does not bind every original indexed check.',task_id=tid)
            if item.get('status')=='NOT_COLLECTED':
                c.require(item.get('recorded_trace_path') is None and item.get('verified_receipt_path') is None and need.get('status')=='NOT_COLLECTED' and need.get('observed_checks_passed') is None and need.get('model_visible_sha256') is None,'uncollected_has_no_fabricated_results','Uncollected queue row contains purported trace/check outcomes.',task_id=tid)
        family_count=len({r.get('workflow_group_id') for r in queue})
        c.require(total_checks==collection_manifest.get('required_checks_total') and len(queue)==collection_manifest.get('task_count') and family_count==collection_manifest.get('workflow_group_count'),'collection_aggregate_counts','Collection totals disagree with inspected artifacts.')
        domain_plan=c.load(collection_root/'domain_collection_plan.json') or {}
        for plan in domain_plan.get('domains',[]):
            expected_ids={tid for tid in train_ids_for_queue if working_records[tid]['domain']==plan.get('domain')}
            c.require(set(plan.get('task_ids',[]))==expected_ids and plan.get('task_count')==len(expected_ids),'collection_domain_plan','Domain plan changes training membership.',domain=plan.get('domain'))
        collection.update({'workflow_groups':family_count,'required_indexed_checks':total_checks,'manifest_sha256':file_hash(collection_root/'collection_manifest.json'),'all_statuses_not_collected':all(r.get('status')=='NOT_COLLECTED' for r in queue),'source_membership_and_hash_links_checked':True})

    # Only the canonical real corpus counts. Documentation and synthetic fixtures do not.
    traces_path=ROOT/'data/sft/reviewed_traces.jsonl';prepared_path=ROOT/'data/sft/prepared/prepared_manifest.json'
    raw_traces=c.jsonl(traces_path,required=False);trace_ids=[r.get('source_task_id') for r in raw_traces];train_ids=set(manifest.get('task_ids',{}).get('train',[]))
    trace_counts={'canonical_file_present':traces_path.is_file(),'rows':len(raw_traces),'unique_training_ids':len(set(trace_ids)&train_ids),'missing_training_ids':len(train_ids-set(trace_ids)),'nontraining_or_unknown_ids':len(set(trace_ids)-train_ids),'schema_and_receipt_validated':False,'valid_complete_workflows':0,'actual_receipt_files':0,'external_verification_authenticated_or_replayed':False}
    receipt_paths=set();receipt_path_problems=[]
    for trace in raw_traces:
        rr=trace.get('review',{}).get('verifier_receipt',{}) if isinstance(trace.get('review'),dict) else {}
        name=rr.get('path')
        if isinstance(name,str):
            candidate=Path(name) if Path(name).is_absolute() else traces_path.parent/name
            try:
                path=local_path(candidate)
                if path.is_file():receipt_paths.add(path)
                else:receipt_path_problems.append('missing')
            except ValueError:receipt_path_problems.append('outside_workspace')
    trace_counts['actual_receipt_files']=len(receipt_paths);trace_counts['receipt_path_problems']=dict(collections.Counter(receipt_path_problems))
    if raw_traces and not receipt_path_problems:
        try:
            preparer=import_local(ROOT/'scripts/prepare_sft.py','foundation_preparer')
            verified,receipts,_=preparer.read_reviewed_traces(traces_path,metadata/'split_manifest.json',ROOT/'data/evaluator_only/train.jsonl')
            trace_counts.update({'schema_and_receipt_validated':True,'valid_complete_workflows':len(verified),'receipt_bindings':len(receipts)})
        except Exception as e:trace_counts['validation_failure']={'type':type(e).__name__,'message':str(e)[:500]}
    prepared={'manifest_present':prepared_path.is_file(),'ready':False,'actual_token_rows':0,'processed_tokens':0,'supervised_tokens':0}
    if prepared_path.is_file():
        pm=c.load(prepared_path) or {};name=pm.get('train_file','')
        if isinstance(name,str) and Path(name).name==name and name:
            tp=prepared_path.parent/name;token_rows=c.jsonl(tp,required=False);prepared['actual_token_rows']=len(token_rows)
            prepared['processed_tokens']=sum(len(r.get('input_ids',[])) for r in token_rows if isinstance(r.get('input_ids'),list))
            prepared['supervised_tokens']=sum(sum(x!=-100 for x in r.get('labels',[])) for r in token_rows if isinstance(r.get('labels'),list))
            try:
                if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
                worker=import_local(ROOT/'train_worker.py','foundation_training_gate')
                detail=worker.validate_prepared_dataset(tp,prepared_path,worker.load_config(ROOT/'config/training.json'),frozen_split_manifest_path=metadata/'split_manifest.json')
                prepared.update({'ready':bool(detail.get('ready')),'validation':detail})
                if traces_path.is_file():c.require(pm.get('source_traces_sha256')==file_hash(traces_path),'prepared_trace_hash','Prepared tokens do not bind current trace file.')
                c.require(pm.get('training_contracts_sha256')==file_hash(ROOT/'data/evaluator_only/train.jsonl'),'prepared_contract_hash','Prepared tokens use different working training contracts.')
            except Exception as e:prepared['validation_failure']={'type':type(e).__name__,'message':str(e)[:500]}
        else:prepared['validation_failure']={'message':'Unsafe or absent token filename'}
    if not trace_counts['schema_and_receipt_validated']:prepared['ready']=False

    files,external_symlinks=bounded_file_inventory();c.require(not external_symlinks,'external_symlink','Portable workspace contains symlinks leaving its root.',paths=external_symlinks)
    tokenizer_files=[p for p in files if p.name in {'tokenizer.json','tokenizer_config.json','vocab.json','merges.txt','special_tokens_map.json'}]
    local_seed_paths=[p for p in files if p.suffix.lower() in {'.sql','.db','.sqlite','.sqlite3'} and 'source_release' not in p.parts]
    seed_archives=[];archive_members=set()
    for p in files:
        if p.suffix=='.zip' and ('gym' in p.name.casefold() or 'seed' in p.name.casefold() or 'environment' in p.name.casefold()):
            try:
                with zipfile.ZipFile(p) as z:
                    members=[x.filename.replace('\\','/') for x in z.infolist() if not x.is_dir()]
                    seeds=[x for x in members if x.endswith(('.sql','.sqlite','.db','.sqlite3'))];archive_members.update(seeds)
                    seed_archives.append({'path':rel(p),'bytes':p.stat().st_size,'sha256':file_hash(p),'seed_members':len(seeds)})
            except (OSError,zipfile.BadZipFile):c.errors.append({'code':'invalid_seed_archive','path':rel(p)})
    available_seed_names=archive_members|{rel(p) for p in local_seed_paths}
    covered_seeds={seed for seed in required_seeds if any(name==seed or name.endswith('/'+seed) for name in available_seed_names)}
    definitions=[p for p in files if p.name in {'Dockerfile','compose.yaml','compose.yml','docker-compose.yaml','docker-compose.yml'} or (p.suffix=='.py' and ('server' in p.stem.casefold() or 'backend' in p.stem.casefold()) and 'tests' not in p.parts)]
    catalog_candidates=[p for p in files if p.suffix in {'.json','.jsonl'} and any(word in p.name.casefold() for word in ['tool_catalog','tool_schemas','mcp_catalog']) and 'reports' not in p.parts]
    assets={'required_unique_seed_references':len(required_seeds),'seed_references_present_by_path':len(covered_seeds),'missing_seed_references':sorted(required_seeds-covered_seeds),'actual_seed_files':[{'path':rel(p),'bytes':p.stat().st_size} for p in local_seed_paths],'actual_seed_archives':seed_archives,'required_server_names':sorted(required_servers),'selected_tool_names':len(selected_tools),'actual_backend_definitions':[{'path':rel(p),'bytes':p.stat().st_size} for p in definitions],'actual_tool_catalog_candidates':[{'path':rel(p),'bytes':p.stat().st_size,'sha256':file_hash(p)} for p in catalog_candidates],'runtime_probed_by_this_checker':False,'runtime_verified':False,'note':'File presence is evidence of assets only, not a functioning MCP service. No Docker or network call is made.'}
    tokenizer_status={'pinned_revision':model_revision,'training_template_present':template.is_file(),'training_template_sha256':file_hash(template) if template.is_file() else None,'historical_synthetic_smoke':historical_tokenizer,'actual_portable_tokenizer_files':[{'path':rel(p),'bytes':p.stat().st_size,'sha256':file_hash(p)} for p in tokenizer_files],'local_pinned_tokenizer_loaded_by_this_check':False,'note':'Historical tokenizer smoke is retained evidence, not a fresh load and not128 real trajectories. No global cache or path outside this folder is inspected.'}

    portable_tokenizer_manifest_path=ROOT/'data/tokenizer/manifest.json'
    portable_tokenizer_manifest=c.load(portable_tokenizer_manifest_path,required=False) or {}
    portable_tokenizer_verified=0;portable_tokenizer_bytes=0
    if portable_tokenizer_manifest:
        c.require(portable_tokenizer_manifest.get('model_id')==config.get('model_id') and portable_tokenizer_manifest.get('model_revision')==model_revision and portable_tokenizer_manifest.get('tokenizer_revision')==model_revision,'portable_tokenizer_revision','Portable tokenizer revision does not match the pinned model.')
        tokenizer_root=local_path(portable_tokenizer_manifest.get('local_model_path','data/tokenizer/MISSING'))
        for name,entry in portable_tokenizer_manifest.get('files',{}).items():
            path=tokenizer_root/name
            if c.check_hash(path,entry.get('sha256'),'portable_tokenizer_file_hash'):
                c.require(path.stat().st_size==entry.get('bytes'),'portable_tokenizer_file_size','Portable tokenizer bytes differ from manifest.',path=rel(path))
                portable_tokenizer_verified+=1;portable_tokenizer_bytes+=path.stat().st_size
        c.require({'tokenizer.json','tokenizer_config.json','chat_template.jinja'}<=set(portable_tokenizer_manifest.get('files',{})),'portable_tokenizer_file_inventory','Pinned portable tokenizer lacks tokenizer data/config/template.')
    tokenizer_status.update({'portable_manifest_present':bool(portable_tokenizer_manifest),'portable_manifest_sha256':file_hash(portable_tokenizer_manifest_path) if portable_tokenizer_manifest_path.is_file() else None,'portable_files_hash_verified':portable_tokenizer_verified,'portable_bytes_hash_verified':portable_tokenizer_bytes,'portable_files_ready':portable_tokenizer_verified>=3 and bool(portable_tokenizer_manifest),'recorded_versions':portable_tokenizer_manifest.get('versions',{}),'model_weights_downloaded_by_this_check':False})

    # Recheck actual relocated environment artifacts; published image metadata is not a pulled image.
    env_source_path=ROOT/'data/environment/source_manifest.json'
    env_source=c.load(env_source_path,required=False) or {};training_seed_entries=env_source.get('training_seed_files',[])
    verified_training_seeds=set();training_seed_bytes=0
    for entry in training_seed_entries:
        path=local_path(entry.get('local_path','data/environment/MISSING'))
        if c.check_hash(path,entry.get('sha256'),'training_seed_file_hash'):
            c.require(path.stat().st_size==entry.get('bytes'),'training_seed_file_size','Seed bytes differ from source manifest.',path=rel(path))
            verified_training_seeds.add(entry.get('source_seed_path'));training_seed_bytes+=path.stat().st_size
    if env_source:
        c.require(verified_training_seeds==required_training_seeds,'training_seed_coverage','Extracted seed metadata does not cover exactly the training-only references.')
        c.require(len(training_seed_entries)==env_source.get('training_seed_count'),'training_seed_count','Training seed count differs from source manifest.')
        for name,entry in env_source.get('artifacts',{}).items():
            artifact=ROOT/'data/environment/source'/name
            c.check_hash(artifact,entry.get('sha256'),'environment_source_artifact_hash')
            if artifact.is_file():c.require(artifact.stat().st_size==entry.get('bytes'),'environment_source_artifact_size','Environment artifact bytes differ.',path=rel(artifact))
    env_config_path=ROOT/'config/local_environment.json'
    env_config=c.load(env_config_path,required=False) or {};server_config=env_config.get('servers',{})
    image_manifest_path=ROOT/'data/environment/image_manifest.json'
    image_manifest=c.load(image_manifest_path,required=False) or {};images=image_manifest.get('images',[]);image_by_domain={x.get('domain'):x for x in images}
    if env_config:
        c.require(set(server_config)==required_servers,'server_configuration_coverage','Pinned server configuration does not match task server identities.')
        for name,entry in server_config.items():
            pin=entry.get('image','');digest=pin.split('@',1)[1] if '@' in pin else ''
            c.require(re.fullmatch(r'sha256:[0-9a-f]{64}',digest) is not None,'pinned_backend_image','Server image is not pinned by digest.',server=name)
            published=image_by_domain.get(entry.get('domain'),{})
            c.require(digest==published.get('digest') and entry.get('platform')=='linux/amd64','backend_image_manifest_binding','Server image digest/platform differs from bundled publisher manifest.',server=name)
            c.require(entry.get('url','').startswith(('http://localhost:','http://127.0.0.1:')),'local_server_endpoint','Foundation endpoint must remain local.',server=name)
        definitions.append(env_config_path)
    doctor_path=ROOT/'reports/local_environment_status.json';doctor=c.load(doctor_path,required=False) or {}
    doctor_summary={'report_present':doctor_path.is_file(),'report_sha256':file_hash(doctor_path) if doctor_path.is_file() else None,'recorded_at':doctor.get('created_utc'),'workspace_matches':doctor.get('workspace')==str(ROOT),'docker':doctor.get('docker',{}),'servers_reported':len(doctor.get('servers',[])),'servers_recorded_tcp_reachable':sum(x.get('tcp_reachable') is True for x in doctor.get('servers',[])),'recorded_backend_verified':doctor.get('backend_verified',False),'independent_current_probe_by_foundation_checker':False}
    if doctor:
        c.require(doctor.get('workspace')==str(ROOT),'doctor_workspace','Local environment report belongs to another folder.')
        c.require(set(x.get('path') for x in doctor.get('seed_files',[]))==set(x.get('local_path') for x in training_seed_entries),'doctor_seed_inventory_binding','Doctor report covers another seed inventory.')
    assets.update({'environment_source_manifest_present':bool(env_source),'pinned_repository_revision':env_source.get('revision'),'training_seed_references_required':len(required_training_seeds),'training_seed_references_hash_verified':len(verified_training_seeds),'training_seed_bytes_hash_verified':training_seed_bytes,'training_seed_files_match_exact_training_scope':verified_training_seeds==required_training_seeds,'pinned_server_configuration_present':bool(env_config),'pinned_server_count':len(server_config),'published_image_digest_records':len(images),'published_images_are_not_local_container_evidence':True,'local_environment_doctor':doctor_summary,'actual_backend_definitions':[{'path':rel(p),'bytes':p.stat().st_size} for p in definitions]})
    deferred_path=ROOT/'work/deferred_modal_files_sha256.json';deferred=c.load(deferred_path,required=False) or {}
    for name,expected in deferred.items():c.check_hash(ROOT/name,expected,'deferred_modal_files_unchanged')
    assets['deferred_modal_files_checked']=len(deferred)

    holds=c.load(metadata/'quality_holds.json') or {};held_tasks=holds.get('tasks',[])
    for hold in held_tasks:c.require(hold.get('task_id') in active and roles.get(hold['task_id'])==hold.get('role'),'quality_hold_membership','Known semantic hold changed frozen membership.')
    settings=c.load(ROOT/'config/modal.json') or {};caps=settings.get('campaign_caps_usd',{});ledger_path=ROOT/'runs/budget_ledger.json'
    ledger=c.load(ledger_path,required=False)
    total_cap=Decimal(str(caps.get('total','0')));buckets={k:Decimal(str(caps.get(k,'0'))) for k in ['teacher_api','gpu_compute','other_modal']}
    c.require(total_cap==Decimal('40.00') and sum(buckets.values())<=total_cap and all(v>=0 for v in buckets.values()),'campaign_cap','Campaign cap must remain40 and buckets may not exceed it.')
    if ledger is None:budget={'ledger_present':False,'recorded_calls':0,'recorded_accounted_or_reserved_usd':None,'reason':'No campaign ledger file exists locally. Do not infer verified zero provider usage or reset prior spend.','provider_billing_checked':False}
    else:
        calls=ledger.get('calls',[]);reserved=sum((Decimal(str(x.get('reserved_usd','0'))) for x in calls),Decimal('0'));api=Decimal(str(ledger.get('teacher_api_spent_usd','0')));other=Decimal(str(ledger.get('other_modal_spent_usd','0')))
        budget={'ledger_present':True,'ledger_sha256':file_hash(ledger_path),'recorded_calls':len(calls),'reserved_compute_usd':str(reserved),'teacher_api_spent_usd':str(api),'other_spent_usd':str(other),'recorded_accounted_or_reserved_usd':str(reserved+api+other),'pending_calls':[x.get('run_id') for x in calls if x.get('status')=='reserved'],'provider_billing_checked':False}
        c.require(reserved<=buckets['gpu_compute'] and api<=buckets['teacher_api'] and other<=buckets['other_modal'] and reserved+api+other<=total_cap,'recorded_budget_within_cap','Recorded spend/reservations exceed a campaign cap.')
    budget.update({'authorized_campaign_cap_usd':str(total_cap),'authorized_buckets_usd':{k:str(v) for k,v in buckets.items()},'spending_performed_by_this_checker':False,'cloud_preparation_status':'DEFERRED_BY_USER','note':'Configuration and any ledger are local records, not live billing evidence. No remote cap/authentication is checked or changed.'})

    missing=[]
    if trace_counts['valid_complete_workflows']!=128:missing.append('128 complete reviewed training-only trajectories with bound real verifier receipts')
    if not prepared['ready']:missing.append('Verified prepared training tokens and prepared_manifest.json')
    if not collection_manifest or len(queue)!=128:missing.append('Complete128-task training-only collection queue with provenance links')
    if len(covered_seeds)<len(required_seeds):missing.append('Locally present matching seed database assets for every required reference')
    if not definitions:missing.append('Local MCP backend source/deployment definitions')
    if doctor and not doctor.get('docker',{}).get('daemon_reachable'):missing.append('Running local container runtime and MCP services; recorded Docker daemon probe is unavailable')
    if not catalog_candidates:missing.append('Actual tool schema/catalog artifacts from the enterprise backends')
    missing.append('Controlled local environment reset/tool/verifier replay evidence; not established by file presence')
    if held_tasks:missing.append('Resolution of the retained semantic scorer hold before a complete final-evaluation claim')
    if not tokenizer_status['portable_files_ready']:missing.append('Complete portable pinned tokenizer assets with verified hashes')
    integrity=not c.errors
    data_ready=trace_counts['valid_complete_workflows']==128 and prepared['ready']
    readiness={'integrity_passed':integrity,'source_task_specifications_present':len(active)==329,'verified_sft_workflows':trace_counts['valid_complete_workflows'],'sft_ready':data_ready,'foundation_files_ready':integrity and bool(env_config) and verified_training_seeds==required_training_seeds and tokenizer_status['portable_files_ready'] and bool(trace_schema) and bool(receipt_schema) and bool(collection_manifest) and len(queue)==128,'runtime_environment_ready':False,'final_evaluation_ready':False if held_tasks else None,'foundation_complete_for_training':integrity and data_ready,'modal_preparation':'deferred','known_semantic_holds':len(held_tasks)}
    status='INTEGRITY_FAILURE' if c.errors else ('LOCAL_SFT_ARTIFACTS_READY_RUNTIME_SEPARATE' if readiness['foundation_complete_for_training'] else 'NOT_READY_MISSING_ARTIFACTS')
    historical_paths=[]
    for report_name in ['dataset_audit.json','validation_summary.json']:
        report=c.load(ROOT/'reports'/report_name,required=False) or {}
        for key in ['working_folder','dataset_path','payload_root']:
            value=report.get(key)
            if isinstance(value,str) and value.startswith('/') and not value.startswith(str(ROOT)):
                historical_paths.append({'report':'reports/'+report_name,'field':key,'recorded_path':value,'interpretation':'Historical location; current files independently checked here. Historical reports were not rewritten.'})
    report={'schema_version':1,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'workspace_root':str(ROOT),'status':status,'scope':'Noncloud local foundation audit; metadata, opaque record replay, hashes and actual file inventory. No final-test question/SQL interpretation, model outputs, paid APIs, GPU or Docker execution.','readiness':readiness,'dataset':{'frozen_manifest_sha256':file_hash(source/'split_manifest.json'),'selected_unique_tasks':len(active),'split_counts':{r:len(manifest.get('task_ids',{}).get(r,[])) for r in ROLES},'domain_counts_by_role':domain_counts,'excluded_tasks':len(excluded),'prior_quarantined_tasks':len(quarantined),'copy_counts_not_extra_examples':copy_counts,'normalization_replayed':len(changes),'normalization_counts':dict(changes_by_kind),'active_workflow_groups':group_count,'source_family_audits':source_family_audits},'schemas':{'trace_schema_present':bool(trace_schema),'receipt_schema_present':bool(receipt_schema),'trace_schema_sha256':file_hash(ROOT/'config/trace_schema.json'),'receipt_schema_sha256':file_hash(ROOT/'config/verifier_receipt.schema.json'),'receipt_schema_version':receipt_schema.get('properties',{}).get('schema_version',{}).get('const'),'per_index_outcomes_required':'outcomes' in receipt_schema.get('required',[])},'collection_queue':collection,'reviewed_training_data':trace_counts,'prepared_training_data':prepared,'tokenizer':tokenizer_status,'environment_assets':assets,'known_quality_holds':[{'task_id':h.get('task_id'),'role':h.get('role'),'status':h.get('status')} for h in held_tasks],'budget':budget,'integrity_errors':c.errors,'check_counts':dict(c.checks),'missing_or_unverified':missing,'historical_report_paths':historical_paths,'limitations':['This check does not authenticate external review receipts or independently replay task outcomes.','Current file hashes are checked directly. The separate local doctor report is recorded probe evidence, not a fresh network/daemon probe by this checker.','The absence of a local budget ledger is not proof of zero spending in a provider account.','A copied task specification is not an additional training example; only validated real trajectories count.','Cloud work remains deferred.']}
    out=ROOT/'reports';out.mkdir(exist_ok=True)
    (out/'foundation_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    done=[f'Frozen329 unique task specifications preserved:128train /41development /160test.',f'Immutable source-copy hashes and {len(changes)} recorded working normalizations checked.',f'{group_count} active workflow groups and both source family-audit files checked for split isolation.',f'Training-only collection queue: {len(queue)} tasks, {collection.get("workflow_groups",0)} families and {collection.get("required_indexed_checks",0)} indexed check requirements; status counts {collection["status_counts"]}.', 'Trace and receipt schemas plus pinned model/template configuration are present.','$40 campaign configuration checked without spending or remote account access.']
    md=['# Local foundation audit','',f'**{status}** — checked {str(ROOT)}.','',f'Foundation files ready: **{readiness["foundation_files_ready"]}**. Integrity errors: **{len(c.errors)}**. Validated real SFT workflows: **{trace_counts["valid_complete_workflows"]}/128**. Prepared training rows: **{prepared["actual_token_rows"]}**.','', '## Verified locally','']
    md+=['- '+x for x in done] if not c.errors else ['- Integrity verification found errors; see details below.']
    md+=['','## Missing or unverified','']+['- '+x for x in missing]
    md+=['','## Actual environment files','',f'- Required unique seed references: {len(required_seeds)}; present by matching local/archive path: {len(covered_seeds)}.',f'- Seed files: {len(local_seed_paths)}; seed archives: {len(seed_archives)}; backend definitions: {len(definitions)}; tool catalog artifacts: {len(catalog_candidates)}.',f'- Training-specific seeds freshly hash-verified: {len(verified_training_seeds)}/{len(required_training_seeds)} ({training_seed_bytes:,} bytes); pinned server images: {len(server_config)}. Published digest records are not locally running containers.',f'- Local doctor report: Docker daemon reachable={doctor.get("docker",{}).get("daemon_reachable","unverified")}; {doctor_summary["servers_recorded_tcp_reachable"]}/{doctor_summary["servers_reported"]} server ports reachable at its recorded check. No new probe by this checker.',f'- Portable tokenizer files freshly hash-verified: {portable_tokenizer_verified} ({portable_tokenizer_bytes:,} bytes), pinned to {model_revision}. A historical synthetic tokenizer smoke is recorded; no tokenizer was loaded by this check.','', '## Readiness and scope','','The source questions and frozen split are organized. They are not a verified training corpus. Training remains blocked until real reviewed trajectories, bound receipts, and validated prepared tokens exist. The known final-test scorer hold remains in membership and prevents a complete final-evaluation claim. The other tasks are not thereby semantically certified.','', 'This check made no cloud, Docker, GPU, model, tokenizer-download, or spending call. Modal preparation remains deferred. Historical reports were preserved; this report records the current folder.','', '## Budget','',f'- Authorized campaign cap: ${total_cap}; moving folders or accounts does not reset it.', '- Provider billing was not queried. '+('Local ledger totals are shown in the JSON report.' if ledger is not None else 'No local ledger file exists; this is not evidence of zero provider spending.'),'', '## Reproduce','', '```bash','python3 scripts/foundation_check.py','```','', 'Exit2 means missing/not-ready SFT artifacts; exit1 means integrity failure. Exit0 certifies local SFT artifact checks only; runtime, known final-evaluation holds and deferred cloud work remain separate. The command writes only these foundation reports.']
    if c.errors:md+=['','## Integrity errors','']+['- '+canonical(e) for e in c.errors]
    (out/'foundation_audit.md').write_text('\n'.join(md)+'\n')
    print(json.dumps(report if args.json else {'status':status,'workspace_root':str(ROOT),'foundation_files_ready':readiness['foundation_files_ready'],'integrity_errors':len(c.errors),'verified_sft_workflows':trace_counts['valid_complete_workflows'],'prepared_token_rows':prepared['actual_token_rows'],'known_quality_holds':len(held_tasks),'missing_or_unverified':missing},indent=2,ensure_ascii=False))
    return 1 if c.errors else (0 if readiness['foundation_complete_for_training'] else 2)

if __name__=='__main__':raise SystemExit(main())

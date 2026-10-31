#!/usr/bin/env python3
"""Local-first Modal launcher. --plan is offline; --train is explicitly paid work.

Run this script instead of `modal run`: it validates real SFT and budget evidence
before an image build, data upload, or GPU invocation can be dispatched.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from budget_control import load_json,new_ledger,summarize,reserve_call,finish_call

def validate_local(prepared_dir):
    import train_worker
    p=Path(prepared_dir).resolve()
    manifest_path=p/'prepared_manifest.json'
    if not manifest_path.is_file():
        raise ValueError('Verified SFT is not prepared. Task specifications are not training answers. Run scripts/prepare_sft.py on reviewed demonstrations first.')
    manifest=load_json(manifest_path)
    split_path=ROOT/'data/metadata/split_manifest.json'
    split=load_json(split_path)
    if manifest.get('split_manifest_sha256')!=hashlib.sha256(split_path.read_bytes()).hexdigest():
        raise ValueError('Prepared data do not use this frozen task split')
    if manifest.get('training_task_ids')!=sorted(split['task_ids']['train']):
        raise ValueError('Prepared data must cover exactly the frozen training tasks; no test/development data')
    contracts=ROOT/'data/evaluator_only/train.jsonl'
    if manifest.get('training_contracts_sha256')!=hashlib.sha256(contracts.read_bytes()).hexdigest():
        raise ValueError('Prepared review receipts do not use the current normalized training checker contracts')
    config=train_worker.load_config(ROOT/'config/training.json')
    train_name=manifest.get('train_file','')
    if Path(train_name).name!=train_name or not train_name:
        raise ValueError('Unsafe prepared training filename')
    summary=train_worker.validate_prepared_dataset(p/train_name,manifest_path,config)
    return config,manifest,summary

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    action=parser.add_mutually_exclusive_group()
    action.add_argument('--plan',action='store_true',help='Print offline readiness and cost plan (default)')
    action.add_argument('--train',action='store_true',help='Dispatch one budgeted paid Modal training chunk')
    parser.add_argument('--prepared-dir',default=str(ROOT/'data/sft/prepared'))
    parser.add_argument('--run-name',default='qwen35-9b-lora-v1')
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--environment',default=None,help='Modal environment in the active profile')
    args=parser.parse_args()
    settings=load_json(ROOT/'config/modal.json')
    ledger_path=ROOT/'runs/budget_ledger.json'
    ledger=load_json(ledger_path) if ledger_path.exists() else new_ledger()
    readiness={}
    try:
        config,manifest,summary=validate_local(args.prepared_dir)
        readiness=summary
    except (ValueError,OSError,KeyError) as error:
        readiness={'ready':False,'reason':str(error)}
    report={'task_specifications':load_json(ROOT/'data/metadata/split_manifest.json')['counts'],
            'verified_sft':readiness,'budget':summarize(settings,ledger),
            'provider_usage_cap_recorded':settings['budget_enforcement']['platform_usage_cap_configured'],
            'cloud_runtime_tested':settings['cloud_runtime_tested']}
    if not args.train:
        print(json.dumps(report,indent=2));return
    if not readiness.get('ready'):
        parser.error(readiness['reason'])
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}',args.run_name):
        parser.error('Run name must be lowercase letters, numbers, underscores or hyphens')
    if not settings['budget_enforcement']['platform_usage_cap_configured']:
        parser.error('Record the Modal gross usage cap after setting it in Usage & Billing. The authorized campaign total remains $40, including external API costs.')
    if not (os.environ.get('MODAL_TOKEN_ID') and os.environ.get('MODAL_TOKEN_SECRET')):
        cfg=Path(os.environ.get('MODAL_CONFIG_PATH',str(Path.home()/'.modal.toml')))
        if not cfg.is_file(): parser.error('Modal is not authenticated. Use modal token new; never put tokens in this project.')
    # All local checks precede import/build/upload and any GPU allocation.
    if args.environment:
        os.environ['MODAL_ENVIRONMENT']=args.environment
    import modal_app
    prepared=Path(args.prepared_dir).resolve()
    call=reserve_call(settings,ledger_path,run_name=args.run_name,
                      dataset_sha256=manifest['train_file_sha256'],
                      checkpoint='latest' if args.resume else None)
    identity={'model_id':config['model_id'],'model_revision':config['model_revision'],
              'split_manifest_sha256':manifest['split_manifest_sha256'],
              'training_dataset_sha256':manifest['train_file_sha256'],
              'chat_template_sha256':manifest['chat_template_sha256']}
    try:
        # Only tokens, training template and their manifest enter the data Volume.
        # Source tests and evaluator SQL are never uploaded by this launcher.
        with modal_app.data_volume.batch_upload() as batch:
            for name in [manifest['train_file'],'prepared_manifest.json',manifest['chat_template_file']]:
                if Path(name).name!=name: raise ValueError('Unsafe artifact filename')
                batch.put_file(str(prepared/name),f"/{manifest['train_file_sha256']}/{name}")
        with modal_app.app.run(environment_name=args.environment):
            result=modal_app.train_chunk.remote(
                args.run_name,call['run_id'],manifest['train_file_sha256'],
                summary['prepared_manifest_sha256'],config,identity,
                time.time()+settings['function_timeout_seconds'],resume=args.resume)
        finish_call(ledger_path,call['run_id'],'completed',result=result)
        print(json.dumps(result,indent=2))
    except BaseException as error:
        finish_call(ledger_path,call['run_id'],'interrupted_or_failed',
                    result={'error_type':type(error).__name__,'message':str(error)})
        raise

if __name__=='__main__': main()

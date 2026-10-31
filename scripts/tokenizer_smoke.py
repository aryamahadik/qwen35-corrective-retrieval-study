#!/usr/bin/env python3
"""Local tokenizer/mask smoke only. The synthetic fixture is never SFT data."""
from pathlib import Path
import importlib.metadata
import json
import datetime
import prepare_sft

ROOT=Path(__file__).resolve().parents[1]

def main():
    local,manifest=prepare_sft.validate_local_tokenizer()
    versions={k:importlib.metadata.version(k) for k in prepare_sft.EXPECTED_VERSIONS}
    if versions!=prepare_sft.EXPECTED_VERSIONS:
        raise ValueError('Use this folder\'s pinned .venv-prepare environment')
    from transformers import AutoTokenizer
    tokenizer=AutoTokenizer.from_pretrained(local,local_files_only=True,token=False,
                                           trust_remote_code=False,use_fast=True)
    fixture={
        'source_task_id':'SYNTHETIC_FORMAT_TEST_NOT_A_TRAINING_TASK',
        'tools':[{'type':'function','function':{'name':'lookup_fixture',
                 'description':'Synthetic formatting test only.',
                 'parameters':{'type':'object','properties':{'record_id':{'type':'string'}},
                               'required':['record_id'],'additionalProperties':False}}}],
        'messages':[
            {'role':'system','content':'This is a tokenizer formatting fixture, not a real enterprise task.'},
            {'role':'user','content':'Look up the synthetic fixture.'},
            {'role':'assistant','content':'','tool_calls':[{'id':'fixture_call',
              'type':'function','function':{'name':'lookup_fixture','arguments':{'record_id':'fixture'}}}]},
            {'role':'tool','tool_call_id':'fixture_call','name':'lookup_fixture',
             'content':'{"record_id":"fixture","status":"synthetic"}'},
            {'role':'assistant','content':'The synthetic formatting fixture was returned.'}
        ]}
    row=prepare_sft.tokenize_trace(fixture,tokenizer,prepare_sft.TEMPLATE_PATH.read_text(),16384)
    result={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'status':'PASS','scope':'Synthetic local tokenizer/mask check only',
            'model_revision':manifest['model_revision'],'versions':versions,
            'processed_tokens':len(row['input_ids']),
            'supervised_tokens':sum(x!=-100 for x in row['labels'][1:]),
            'first_token_masked':row['labels'][0]==-100,
            'network_used':False,'model_weights_loaded':False,'gpu_used':False,
            'sft_dataset_written':False,'real_demonstrations_generated':0}
    (ROOT/'reports/foundation_tokenizer_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()

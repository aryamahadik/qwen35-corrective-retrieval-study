"""Modal infrastructure. Launch through scripts/launch.py so local gates run first.

Only prepared training tokens are uploaded. The final-test and evaluator-only
files are never mounted in the training container. No work starts on import.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import sys
import time

import modal

LOCAL=Path(__file__).resolve().parent
if str(LOCAL) not in sys.path: sys.path.insert(0,str(LOCAL))
SETTINGS=json.loads((LOCAL/'config/modal.json').read_text())
app=modal.App(SETTINGS['app_name'])
ENVIRONMENT=os.environ.get('MODAL_ENVIRONMENT')
data_volume=modal.Volume.from_name(SETTINGS['data_volume'],create_if_missing=True,environment_name=ENVIRONMENT)
checkpoint_volume=modal.Volume.from_name(SETTINGS['checkpoint_volume'],create_if_missing=True,environment_name=ENVIRONMENT)
cache_volume=modal.Volume.from_name(SETTINGS['model_cache_volume'],create_if_missing=True,environment_name=ENVIRONMENT)

image=(modal.Image.from_registry('nvidia/cuda:12.8.1-devel-ubuntu22.04@sha256:a99a1860ba8e2916e5c3e73b72ec4c4301653a84586e05bfc9a2aa2d58027e97',add_python='3.12')
       .apt_install('git','build-essential')
       .pip_install_from_requirements(str(LOCAL/'requirements-train.txt'))
       .env({'HF_HOME':'/model-cache/huggingface','TOKENIZERS_PARALLELISM':'false',
             'UNSLOTH_RETURN_LOGITS':'0','PYTHONUNBUFFERED':'1',
             'ENTERPRISEOPS_SPLIT_MANIFEST':'/app/split_manifest.json'})
       .add_local_python_source('train_worker','checkpoint_utils',copy=True)
       .add_local_file(LOCAL/'data/metadata/split_manifest.json','/app/split_manifest.json',copy=True))

@app.function(
    image=image, gpu=SETTINGS['gpu'], serialized=True, include_source=False,
    cpu=(SETTINGS['physical_cpu_cores'],SETTINGS['physical_cpu_cores']),
    memory=(SETTINGS['memory_gib']*1024,SETTINGS['memory_gib']*1024),
    volumes={'/training-data':data_volume.with_mount_options(read_only=True),
             '/checkpoints':checkpoint_volume,'/model-cache':cache_volume},
    min_containers=0, max_containers=1, buffer_containers=0,
    scaledown_window=2, single_use_containers=True, retries=0,
    timeout=SETTINGS['function_timeout_seconds'],
    startup_timeout=SETTINGS['startup_timeout_seconds'],
)
def train_chunk(run_name: str, call_id: str, dataset_key: str,
                prepared_manifest_sha256: str, config: dict,
                checkpoint_identity: dict, absolute_deadline_unix: float,
                resume: bool = False) -> dict:
    import train_worker
    import checkpoint_utils
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}',run_name):
        raise ValueError('Unsafe run name')
    if not re.fullmatch(r'[0-9a-f]{32}',call_id) or not re.fullmatch(r'[0-9a-f]{64}',dataset_key):
        raise ValueError('Invalid call or dataset identity')
    # Absolute deadline is supplied once and persists through automatic input
    # restarts. retries=0 alone does not prevent Modal preemption restarts.
    if time.time() >= absolute_deadline_unix-180:
        raise ValueError('This reserved invocation has no remaining checkpoint-safe time')
    data=Path('/training-data')/dataset_key
    manifest_path=data/'prepared_manifest.json'
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest()!=prepared_manifest_sha256:
        raise ValueError('Remote prepared-manifest hash differs from the staged artifact')
    prepared=json.loads(manifest_path.read_text())
    run=Path('/checkpoints/runs')/run_name
    run.mkdir(parents=True,exist_ok=True)
    config_path=run/'training_config.json'
    if config_path.exists() and json.loads(config_path.read_text())!=config:
        raise ValueError('Existing run training configuration differs')
    config_path.write_text(json.dumps(config,indent=2)+'\n')
    loaded=train_worker.load_config(config_path)
    summary=train_worker.validate_prepared_dataset(data/prepared['train_file'],manifest_path,loaded)
    if summary['train_file_sha256']!=dataset_key:
        raise ValueError('Staged data folder does not match training-file hash')
    for key,expected in [('model_id',config['model_id']),('model_revision',config['model_revision']),
                         ('training_dataset_sha256',dataset_key),
                         ('split_manifest_sha256',prepared['split_manifest_sha256']),
                         ('chat_template_sha256',prepared['chat_template_sha256'])]:
        if checkpoint_identity.get(key)!=expected:
            raise ValueError(f'Checkpoint identity mismatch: {key}')
    complete=checkpoint_utils.latest_checkpoint(run,checkpoint_identity)
    result_path=run/'training_result.json'
    if result_path.exists():
        previous=json.loads(result_path.read_text())
        if previous.get('status')=='EPOCH_COMPLETE':
            if complete is None: raise ValueError('Completed run has no valid complete checkpoint')
            return {**previous,'already_complete':True,'checkpoint_path':str(complete)}
    # A preemption restart of this same call may find a checkpoint even if the
    # initial user invocation was not --resume. Explicit fresh calls cannot.
    invocation=run/'invocations'/f'{call_id}.json'
    restarted=invocation.exists()
    if complete is not None and not (resume or restarted):
        raise ValueError('Existing checkpoint found; resume explicitly or choose another run name')
    if resume and complete is None:
        raise ValueError('Resume requested but no verified complete checkpoint was found')
    checkpoint_utils.quarantine_unpublished_checkpoints(
        run,checkpoint_identity,commit=checkpoint_volume.commit)
    invocation.parent.mkdir(parents=True,exist_ok=True)
    invocation.write_text(json.dumps({'call_id':call_id,'absolute_deadline_unix':absolute_deadline_unix,
                                     'dataset_key':dataset_key,'started_unix':time.time()},indent=2)+'\n')
    checkpoint_volume.commit()
    def publish(path):
        checkpoint_utils.publish_checkpoint(path,checkpoint_identity,commit=checkpoint_volume.commit)
    remaining=int(absolute_deadline_unix-time.time())-60
    duration=min(SETTINGS['soft_training_session_seconds'],remaining)
    if duration<=loaded['checkpoint_reserve_seconds']:
        raise ValueError('No remaining safe training interval')
    try:
        result=train_worker.run_training(str(data/prepared['train_file']),str(run),
            prepared_manifest_path=str(manifest_path),config_path=str(config_path),
            resume_from_checkpoint=str(complete) if complete else None,
            on_checkpoint=publish,max_wall_seconds=duration)
        checkpoint_volume.commit();cache_volume.commit()
        return result
    finally:
        # Commits persist diagnostic files, but only published complete
        # checkpoints can be used by latest_checkpoint().
        checkpoint_volume.commit()
        cache_volume.commit()

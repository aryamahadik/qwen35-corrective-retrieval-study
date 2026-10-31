"""Conservative local reservations, not a substitute for Modal's usage cap.

Completed and interrupted calls retain their reservation until manually reconciled
against the provider's bill. Copy this ledger when moving accounts. No network I/O.
"""
from contextlib import contextmanager
from decimal import Decimal, ROUND_CEILING
from pathlib import Path
import datetime
import fcntl
import json
import os
import uuid

def load_json(path):
    return json.loads(Path(path).read_text())

def atomic_json(path, value):
    path=Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp=path.with_name(path.name+'.tmp')
    with tmp.open('w') as stream:
        json.dump(value,stream,indent=2)
        stream.write('\n');stream.flush();os.fsync(stream.fileno())
    os.replace(tmp,path)

def rate_per_second(config):
    prices=config['prices_usd_per_second']
    return (Decimal(prices['gpu_a100_80gb'])
            +Decimal(prices['physical_cpu_core'])*config['physical_cpu_cores']
            +Decimal(prices['memory_gib'])*config['memory_gib'])

def reservation_cost(config):
    seconds=(config['function_timeout_seconds']
             +config['startup_timeout_seconds']+config['billing_tail_allowance_seconds'])
    return (rate_per_second(config)*seconds).quantize(Decimal('.01'),rounding=ROUND_CEILING)

def new_ledger():
    return {'schema_version':1,'campaign_id':'enterpriseops-40usd-v1',
            'teacher_api_spent_usd':'0','other_modal_spent_usd':'0',
            'calls':[],'note':'Reservation accounting; not live provider billing. Retain across accounts.'}

def summarize(config, ledger):
    caps=config['campaign_caps_usd']
    reserved=sum((Decimal(x['reserved_usd']) for x in ledger['calls']),Decimal(0))
    api=Decimal(ledger['teacher_api_spent_usd'])
    other=Decimal(ledger['other_modal_spent_usd'])
    return {'hourly_requested_resource_rate_usd':str(rate_per_second(config)*3600),
            'one_call_reservation_usd':str(reservation_cost(config)),
            'reserved_gpu_usd':str(reserved),
            'remaining_gpu_reservation_usd':str(Decimal(caps['gpu_compute'])-reserved),
            'teacher_api_spent_usd':str(api),'other_modal_spent_usd':str(other),
            'accounted_or_reserved_total_usd':str(reserved+api+other),
            'campaign_cap_usd':caps['total'],
            'pending_calls':[x['run_id'] for x in ledger['calls'] if x['status']=='reserved']}

@contextmanager
def locked_ledger(path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.with_suffix('.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        ledger=load_json(path) if path.exists() else new_ledger()
        yield ledger
        atomic_json(path,ledger)

def reserve_call(config, ledger_path, *, run_name, dataset_sha256, checkpoint=None):
    caps=config['campaign_caps_usd']
    if Decimal(caps['total'])>40 or sum(Decimal(caps[k]) for k in ['teacher_api','gpu_compute','other_modal'])>Decimal(caps['total']):
        raise ValueError('Budget exceeds the authorized $40 campaign.')
    with locked_ledger(ledger_path) as ledger:
        s=summarize(config,ledger)
        if s['pending_calls']:
            raise ValueError('A previous call is unresolved. Check its status before starting another.')
        amount=reservation_cost(config)
        if amount>Decimal(s['remaining_gpu_reservation_usd']):
            raise ValueError('Insufficient unreserved compute budget for another complete call.')
        if Decimal(ledger['teacher_api_spent_usd'])>Decimal(caps['teacher_api']) or Decimal(ledger['other_modal_spent_usd'])>Decimal(caps['other_modal']):
            raise ValueError('A non-GPU budget bucket is already exceeded.')
        call={'run_id':uuid.uuid4().hex,'run_name':run_name,
              'dataset_sha256':dataset_sha256,'resume_checkpoint':checkpoint,
              'reserved_usd':str(amount),'status':'reserved',
              'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
        ledger['calls'].append(call)
    return call

def finish_call(ledger_path, run_id, status, *, result=None):
    if status not in {'completed','interrupted_or_failed'}:
        raise ValueError('Unsupported status')
    with locked_ledger(ledger_path) as ledger:
        matches=[x for x in ledger['calls'] if x['run_id']==run_id]
        if len(matches)!=1: raise ValueError('Unknown call reservation')
        matches[0]['status']=status
        matches[0]['result']=result
        # Deliberately keep the whole reservation. Provider invoices are authoritative.


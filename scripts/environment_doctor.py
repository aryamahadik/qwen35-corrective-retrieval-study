#!/usr/bin/env python3
"""Read-only local backend checks. Does not start Docker, containers, or cloud jobs."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import socket
import subprocess
import datetime
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def local_path(relative):
    p=(ROOT/relative).resolve()
    if not p.is_relative_to(ROOT): raise ValueError('Environment asset path escapes this workspace')
    return p

def inspect_environment(probe=True):
    config=json.loads((ROOT/'config/local_environment.json').read_text())
    source=json.loads(local_path(config['source_manifest']).read_text())
    seed_checks=[]
    for entry in source['training_seed_files']:
        p=local_path(entry['local_path'])
        seed_checks.append({'path':entry['local_path'],'exists':p.is_file(),
                            'hash_matches':p.is_file() and sha256(p)==entry['sha256']})
    docker={'cli_available':bool(shutil.which('docker')),'daemon_reachable':False,
            'probe_performed':False,'containers_started':False}
    if probe and docker['cli_available']:
        docker['probe_performed']=True
        try:
            r=subprocess.run(['docker','info','--format','{{json .ServerVersion}}'],
                             cwd=ROOT,capture_output=True,text=True,timeout=8)
            docker['daemon_reachable']=r.returncode==0
            if r.returncode==0: docker['server_version']=r.stdout.strip().strip('"')
            else: docker['reason']='Docker daemon is unavailable to this client; no start was attempted.'
        except (OSError,subprocess.TimeoutExpired):
            docker['reason']='Docker availability check failed or timed out.'
    servers=[]
    for name,spec in sorted(config['servers'].items()):
        u=urlparse(spec['url'])
        if u.hostname not in ('localhost','127.0.0.1','::1'):
            raise ValueError('Only loopback service probes are permitted')
        reachable=False
        if probe:
            try:
                with socket.create_connection((u.hostname,u.port or 80),timeout=.3):reachable=True
            except OSError:pass
        servers.append({'server_name':name,'domain':spec['domain'],'url':spec['url'],
                        'tcp_probe_performed':probe,'tcp_reachable':reachable,
                        'pinned_image':spec['image'],'tool_catalog_verified':False,
                        'sql_runtime_verified':False})
    assets_ok=bool(seed_checks) and all(x['hash_matches'] for x in seed_checks)
    return {'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'workspace':str(ROOT),'scope':'Training-only seed integrity and local service availability',
            'seed_count':len(seed_checks),'seed_files':seed_checks,'seed_assets_valid':assets_ok,
            'docker':docker,'servers':servers,
            'backend_verified':False,'demonstration_collection_ready':False,
            'reason':'TCP reachability is not a verified MCP catalog, schema, reset contract, or successful task execution.',
            'modal_touched':False,'paid_calls':False}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--no-probe',action='store_true')
    p.add_argument('--output',default='reports/local_environment_status.json')
    args=p.parse_args()
    report=inspect_environment(probe=not args.no_probe)
    output=local_path(args.output);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'training_seed_count':report['seed_count'],
                     'seed_assets_valid':report['seed_assets_valid'],
                     'docker_daemon_reachable':report['docker']['daemon_reachable'],
                     'reachable_server_ports':sum(x['tcp_reachable'] for x in report['servers']),
                     'backend_verified':False,'collection_ready':False},indent=2))

if __name__=='__main__':main()

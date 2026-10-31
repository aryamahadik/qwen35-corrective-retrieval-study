#!/usr/bin/env python3
"""Verify/export/import local checkpoint folders after Modal Volume transfer."""
from pathlib import Path
import argparse
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from checkpoint_utils import verify_checkpoint,export_checkpoint,import_checkpoint,latest_checkpoint

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='action',required=True)
    q=sub.add_parser('verify');q.add_argument('checkpoint')
    q=sub.add_parser('export');q.add_argument('checkpoint');q.add_argument('archive')
    q=sub.add_parser('import');q.add_argument('archive');q.add_argument('run_directory')
    q=sub.add_parser('latest');q.add_argument('run_directory')
    args=p.parse_args()
    if args.action=='verify':
        m=verify_checkpoint(args.checkpoint)
        print(json.dumps({'status':m['status'],'step':m['global_step'],'metadata':m['metadata']},indent=2))
    elif args.action=='export': print(export_checkpoint(args.checkpoint,args.archive))
    elif args.action=='import': print(import_checkpoint(args.archive,args.run_directory))
    else: print(latest_checkpoint(args.run_directory))

if __name__=='__main__': main()

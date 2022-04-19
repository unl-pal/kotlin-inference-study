#!/usr/bin/env python
# coding: utf-8

import os.path as osp
import os
import time
import re
import json

from utilities import *

from boaapi.status import CompilerStatus, ExecutionStatus

def query_is_run(target):
    job_data = get_query_data()
    return target in  job_data.keys()

def run_query(target):
    query, query_dataset, make_public = prepare_query(target)
    client = get_client()
    job = client.query(query, client.get_dataset(query_dataset))
    while job.is_running():
        job.refresh()
        print(f"Running job {job.id}.", flush = True)
        time.sleep(10)
    print(f"Job {job.id} is complete.", flush = True)
    if job.compiler_status is CompilerStatus.ERROR:
        print(f"Job {job.id} had a compilation error.", flush = True)
        print(job.get_compiler_errors(), flush = True)
        exit()
    if job.exec_status is ExecutionStatus.ERROR:
        print(f"Job {job.id} had an execution error.", flush = True)
        print(f"See url: {job.get_url()}")
        exit()
    if make_public:
        job.set_public(True)
    update_query_data(target, job.id)

def download_query(target):
    job_data = get_query_data()
    target_job_id = job_data[target]
    client = get_client()
    job = client.get_job(target_job_id)
    with open(target, "w") as fh:
        fh.write(job.output())
    fh.close()

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('target')
    parser.add_argument('--force-rerun', '-force-rerun', '-f')
    args = parser.parse_args()

    target = args.target

    if osp.exists(target):
        print(f"Target file {target} exists.  To re-run query delete the file and pass '--force-rerun'")
        exit()

    if not query_is_run(target) or args.force_rerun:
        run_query(target)

    download_query(target)

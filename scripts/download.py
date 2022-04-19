#!/usr/bin/env python
# coding: utf-8

import os.path as osp
import os
import time
import re
import json

from utilities import *

from boaapi.status import CompilerStatus, ExecutionStatus

def run_query(target):
    config = get_query_config()
    dataset = get_dataset(target)
    make_public = get_make_public(target)
    query, sha256 = prepare_query(target)
    client = get_client()
    job = client.query(query, dataset)
    print(f"Job {job.id} is running.", flush = True)
    job.wait()
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
    update_query_data(target, job.id, sha256)

def download_query(target):
    job_data = get_query_data()
    target_job_id = job_data[target]['job']
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

    if is_run_needed(target):
        run_query(target)

    download_query(target)

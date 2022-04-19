#!/usr/bin/env python
# coding: utf-8

import os.path as osp
import os
import time
import re
import json

from boaapi.boa_client import BoaClient, BOA_API_ENDPOINT
from boaapi.status import CompilerStatus, ExecutionStatus


def get_credentials():
    with open("boa-credentials.txt", "r") as fh:
        creds = [ line.strip() for line in fh.readlines() ]
        user = creds[0]
        password = creds[1]
    fh.close()
    return (user, password)

global client
client = None

def get_client():
    global client
    if client is None:
        username, password = get_credentials()
        client = BoaClient(endpoint = BOA_API_ENDPOINT)
        client.login(username, password)
        return client
    else:
        return client

global config
config = None

def get_query_config():
    global config
    if config is None:
        if osp.exists('job-config.json'):
            with open("job-config.json", "r") as fh:
                query_config = json.load(fh)
                fh.close()
            return query_config
        else:
            print("Job configuration file 'job-config.json' does not exist")
            exit()
    else:
        return config

global job_data
job_data = None

# TODO: Re-read logic & locking
def get_query_data():
    global job_data
    if job_data is None:
        if osp.exists("jobs.json"):
            with open("jobs.json", "r") as fh:
                query_data = json.load(fh)
                fh.close()
            return query_data
        else:
            return {}
    else:
        return job_data

def update_query_data(target, job_id):
    l_job_data = get_query_data()
    l_job_data[target] = job_id
    global job_data
    job_data = l_job_data
    with open("jobs.json", "w") as fh:
        json.dump(l_job_data, fh, indent = 1)
        fh.close()

def query_is_run(target):
    job_data = get_query_data()
    return target in  job_data.keys()

def expand_replacements(replacements, query):
    if len(replacements) > 0:
        has_replaced = True
        while has_replaced:
            has_replaced = False
            for (before, after) in replacements:
                replaced = re.sub(before, after, text)
                if query != replaced:
                    has_replaced = True
                query = replaced
    return query

def build_replacements(global_replacements, local_replacements, only_files=False):
    replacements = {}
    repls = []
    for replacements_list in [local_replacements, global_replacements]:
        for repl in replacements_list:
            target = repl['target']
            if target not in replacements.keys():
                if repl['kind'] == 'text':
                    if not only_files:
                        replacements[target] = repl['replacement']
                else:
                    if only_files:
                        replacements[target] = repl['replacement']
                    else:
                        with open(repl['replacement'], 'r') as fh:
                            replacement = fh.read()
                            fh.close()
                        replacements[target] = replacement
                repls.append((target, replacements[target]))
    return repls

def prepare_query(target):
    config = get_query_config()
    query_info = config['queries'][target]
    query_dataset = config['datasets'][query_info['dataset']]
    query_file = query_info['query']
    with open(query_file, 'r') as fh:
        query = fh.read()
    fh.close()
    query_substitutions = build_replacements(config['substitutions'], query_info['substitutions'])
    query = expand_replacements(query_substitutions, query)
    return query, query_dataset, query_info['make_public']

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

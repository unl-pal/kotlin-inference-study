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
        with open("job-config.json", "r") as fh:
            query_config = json.load(fh)
            fh.close()
        return query_config
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
                query_data = json.load("jobs.json")
                fh.close()
            return query_data
        else:
            return {}
    else:
        return job_data

def update_query_data(target, job_id):
    job_data = get_query_data()
    job_data[target] = job_id
    with open("jobs.json", "w") as fh:
        json.dump(job_data, fh, indent = 1)
        fh.close()

def query_is_run(target):
    job_data = get_query_data()
    return target in  job_data.keys()

def prepare_query(target):
    pass

def run_query(target):
    pass

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
    arguments = parser.parse_args()

    target = arguments.target

    if osp.exists(target):
        print(f"Target file {target} exists.  To re-run query delete the file and pass '--force-rerun'")
        exit()

    if not query_is_run(target) or args.force_rerun:
        run_query(target)

    download_query(target)

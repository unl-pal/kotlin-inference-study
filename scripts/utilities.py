#!/usr/bin/env python
# coding: utf-8

import os.path as osp
import re
import json

from hashlib import sha256


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
    from boaapi.boa_client import BoaClient, BOA_API_ENDPOINT
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

def update_query_data(target, job_id, sha256):
    l_job_data = get_query_data()
    l_job_data[target] = {'job': job_id,
                          'sha256': sha256}
    global job_data
    job_data = l_job_data
    with open("jobs.json", "w") as fh:
        json.dump(l_job_data, fh, indent = 1)
        fh.close()

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

def get_make_public(target):
    config = get_query_config()
    return config['queries'][target]['make_public']

def get_dataset(target):
    config = get_query_config()
    client = get_client()
    dataset_name = config['queries'][target]['dataset']
    if dataset_name in config['datasets'].keys():
        return client.get_dataset(config['datasets'][dataset_name])
    else:
        print(f"Dataset named '{dataset_name}' is not known.", flush = True)
        exit(1)

def prepare_query(target):
    config = get_query_config()
    query_info = config['queries'][target]
    query_file = query_info['query']
    with open(query_file, 'r') as fh:
        query = fh.read()
    fh.close()
    query_substitutions = build_replacements(config['substitutions'], query_info['substitutions'])
    query = expand_replacements(query_substitutions, query)
    return query, sha256(query).hexdigest()

def is_run_needed(target):
    if not osp.exists(target):
        return True
    else:
        query_data = get_query_data()
        if target not in query_data.keys():
            return True
        else:
            hash256 = query_data[target]['sha256']
            _, new256 = prepare_query(target)
            return hash256 != new256

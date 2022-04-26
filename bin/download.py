#!/usr/bin/env python3
# coding: utf-8

# Copyright 2022, Robert Dyer, Samuel W. Flint,
#                 and University of Nebraska Board of Regents
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
from boaapi.status import CompilerStatus, ExecutionStatus
from utilities import *

def run_query(target):
    if not is_run_needed(target):
        return

    client = get_client()
    query, sha256 = prepare_query(target)
    job = client.query(query, get_dataset(target))

    logger.info(f'Job {job.id} is running.')
    job.wait()
    logger.info(f'Job {job.id} is complete.')

    if job.compiler_status is CompilerStatus.ERROR:
        logger.error(f'Job {job.id} had a compilation error.')
        logger.error(job.get_compiler_errors())
        exit(21)
    if job.exec_status is ExecutionStatus.ERROR:
        logger.error(f'Job {job.id} had an execution error.')
        logger.error(f'See url: {job.get_url()}')
        exit(22)

    if get_make_public(target):
        job.set_public(True)

    update_query_data(target, job.id, sha256)

def download_query(target):
    job_data = get_query_data()

    client = get_client()
    job = client.get_job(job_data[target]['job'])

    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, 'w') as fh:
        fh.write(job.output())

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('target')
    parser.add_argument('--force-rerun', '-force-rerun', '-f')
    parser.add_argument('--verbose', '-v', action='count', default = 0)
    args = parser.parse_args()

    verbosity = max(5 - args.verbose, 1) * 10
    logger.setLevel(verbosity)
    logger.info('Setting verbosity to {verbosity}')

    target = args.target

    run_query(target)
    download_query(target)
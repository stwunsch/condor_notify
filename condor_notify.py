#!/usr/bin/env python


import argparse
import subprocess
from time import sleep
import re
import logging
from datetime import datetime
import json


logger = logging.getLogger('condor_notify')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def process_arguments():
    logger.info('Process command line arguments')
    parser = argparse.ArgumentParser(description="Send push notifications of condor job status")
    parser.add_argument('condor_user', type=str,
            help="Condor user name given to `condor_q USERNAME`")
    parser.add_argument('pushover_user', type=str,
            help="Pushover user key")
    parser.add_argument('pushover_token', type=str,
            help="Pushover application token")
    parser.add_argument('--pushover-url', type=str, default='https://api.pushover.net/1/messages.json',
            help="Pushover HTTP request URL")
    parser.add_argument('--sleep', type=float, default=10,
            help="Sleep duration during checking condor job status")
    args = parser.parse_args()

    return args


def get_status(args):
    status = subprocess.check_output(['condor_q', args.condor_user], shell=True)
    return status


def get_status_dict(status):
    lines = [x for x in status.split('\n') if x != '']
    regex = '(?P<jobs>.*) jobs; (?P<completed>.*) completed, (?P<removed>.*) removed, (?P<idle>.*) idle, (?P<running>.*) running, (?P<held>.*) held, (?P<suspended>.*) suspended'
    m = re.search(regex, lines[-1])
    d = {}
    for key in ['jobs', 'completed', 'removed', 'idle', 'running', 'held', 'suspended']:
        if m == None: return None
        else: d[key] = int(m.group(key))
    return d


def check_status(status, status_new):
    d = get_status_dict(status)
    d_new = get_status_dict(status_new)

    if d == None or d_new == None:
        return False

    if d_new['jobs'] < d['jobs']:
        return True

    if d_new['running'] == 0 and d['running'] != 0 and d_new['idle'] == 0:
        return True

    return False


def send_notification(args, status):
    d = get_status_dict(status)
    message = '{}\n'.format(datetime.now())
    for key in d:
        message += '{0} : {1}\n'.format(key, d[key])
    message = message.strip()

    logger.info('Send notification:\n{}'.format(message))
    output = subprocess.check_output([
        'curl',
        '-s',
        '--form-string',
        'token={}'.format(args.pushover_token),
        '--form-string',
        'user={}'.format(args.pushover_user),
        '--form-string',
        'message={}'.format(message),
        args.pushover_url
        ])

    output_dict = json.loads(output)
    if output_dict['status'] != 1:
        logger.error('Return value not 1: {}'.format(output_dict['status']))
        for key in output_dict:
            logger.error('{} : {}'.format(key, output_dict[key]))


if __name__ == '__main__':
    args = process_arguments()
    status = 'no status'
    while True:
        status_new = get_status(args)
        if check_status(status, status_new):
            send_notification(args, status_new)
        status = status_new
        sleep(args.sleep)

#!/usr/bin/env python

import argparse
import re
import json
import os
from dateutil import parser as timeparser
from pprint import pprint


def process_log(fileobj, filename):

    regexes = [
        {'regex': re.compile('^\s*([0-9]{4}-[0-9]{2}-[0-9]{2}T\S+)'), 'name': 'log start time', 'type': ['root']},
        {'regex': re.compile('^\s*([0-9]{4}-[0-9]{2}-[0-9]{2}T\S+)'), 'name': 'log end time', 'type': ['timestamp']},
        {'regex': re.compile('port=([0-9]+)\s'), 'name': 'port', 'type': ['root']},
        {'regex': re.compile('host=(.*)$'), 'name': 'host', 'type': ['root']},
        {'regex': re.compile('\[initandlisten\] db version (v.*)$'), 'name': 'version', 'type': ['root']},
        {'regex': re.compile('New replica set config in use: (.*)$'), 'name': 'replset reconfig', 'type': ['counter']},
        {'regex': re.compile('serverStatus was very slow'), 'name': 'serverStatus was very slow', 'type': ['counter']},
        {'regex': re.compile('SERVER RESTARTED'), 'name': 'server restarted', 'type': ['counter']},
        {'regex': re.compile('COLLSCAN'), 'name': 'collscan', 'type': ['counter']},
        {'regex': re.compile('Starting an election'), 'name': 'election', 'type': ['counter']},
        {'regex': re.compile(' F '), 'name': 'fatal events', 'type': ['counter']},
        {'regex': re.compile(' E '), 'name': 'error events', 'type': ['counter']},
        {'regex': re.compile(' W '), 'name': 'warning events', 'type': ['counter']},
        {'regex': re.compile('build index on'), 'name': 'index build', 'type': ['counter']},
        {'regex': re.compile('op_query [1-9]+[0-9]{3}ms$'), 'name': 'ops > 1000ms', 'type': ['counter']},
        {'regex': re.compile('COMMAND .* replSetStepDown'), 'name': 'replSetStepDown', 'type': ['counter']},
        {'regex': re.compile('step down because I have higher priority'), 'name': 'priority takeover', 'type': ['counter']},
        {'regex': re.compile('\*\*\*aborting after invariant\(\) failure'), 'name': 'invariant failure', 'type': ['counter']},
        {'regex': re.compile('Detected unclean shutdown'), 'name': 'unclean shutdown', 'type': ['counter']}
    ]

    output = {'counters': {}}
    linecount = 0

    for line in fileobj:
        linecount += 1
        for item in regexes:
            match = item['regex'].search(line)
            if match:
                if 'root' in item['type']:
                    regexes.remove(item)
                    output[item['name']] = match.group(1)

                if 'timestamp' in item['type']:
                    output[item['name']] = match.group(1)

                if 'counter' in item['type']:
                    if not output['counters'].get(item['name']):
                        output['counters'][item['name']] = 1
                    else:
                        output['counters'][item['name']] += 1

    output['linecount'] = linecount
    if output.get('log start time') and output.get('log end time'):
        log_start = timeparser.parse(output.get('log start time'))
        log_end = timeparser.parse(output.get('log end time'))
        output['log duration'] = str(log_end - log_start)
    if filename:
        output['filename'] = filename
    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MongoDB log summarizer')
    parser.add_argument('filename', type=str)
    args = parser.parse_args()
    output = process_log(open(os.path.realpath(args.filename)), filename=args.filename)
    pprint(output)

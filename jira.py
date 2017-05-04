#!/usr/bin/env python

import json
import sys
import argparse
import os
import base64
import requests


def do_query(qargs):
    conf_file = get_config()
    auth_string = base64.encodestring((conf_file['config']['user']+":"+conf_file['config']['pass'])).replace('\n', '')
    auth_string = "Basic " + auth_string

    headers = {'Authorization': auth_string,
               'Content-Type': 'application/json'}
    url = conf_file['config']['url'] + "search?jql=" + qargs.query
    r = requests.get(url, headers=headers)
    if args.format == 'json':
        print(r.text)
        sys.exit(0)
    elif qargs.format == 'text':
        json_data = json.loads(r.text)
        for item in json_data['issues']:
            print(item['key'] + " - " + item['fields']['summary'])
    else:
        print("ERROR: Invalid output format specified")
        sys.exit(1)


def get_config():
    if os.path.isfile("config.json"):
        with open("config.json") as conf_file:
            return json.load(conf_file)
    else:
        print("Can't find config.json")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JIRA API test")
    subparsers = parser.add_subparsers()

    parser_query = subparsers.add_parser('query')
    parser_query.add_argument('-q', '--query', required=True)
    parser_query.add_argument('-f', '--format', default='json')
    parser_query.set_defaults(func=do_query)

    args = parser.parse_args()
    args.func(args)

    sys.exit(0)

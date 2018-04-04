#!/usr/bin/env python2

import json
import sys
import argparse
import os
from jira import JIRA


def read_history(jira_con, issue_key, field, verbose):
    issue = jira_con.issue(issue_key, expand='changelog')
    changelog = issue.changelog

    if verbose:
        print(issue.key)

    for history in changelog.histories:
        found_item = False
        for item in history.items:
            if item.field == field:
                if not found_item:
                    print(issue.key)
                    found_item = True
                print('  ' + history.created + ' -- ' + str(item.fromString) + ' to ' + str(item.toString))


def do_query(qargs):
    conf_file = get_config()
    jira = JIRA(conf_file['config']['urlshort'], basic_auth=(conf_file['config']['user'], conf_file['config']['pass']))
    issues = jira.search_issues(qargs.query)
    if qargs.format == 'json':
        print(issues)
    elif qargs.format == 'text':
        for issue in issues:
            print(issue)
    elif qargs.format == 'history':
        for issue in issues:
            read_history(jira, issue.key, qargs.field, qargs.verbose)
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
    parser_query.add_argument('--field', default='status')
    parser_query.add_argument('-v', '--verbose', action='store_true')
    parser_query.set_defaults(func=do_query)

    args = parser.parse_args()
    args.func(args)

    sys.exit(0)

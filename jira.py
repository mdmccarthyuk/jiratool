#!/usr/bin/env python

import json, sys, argparse, os, base64, requests

def doQuery(args):
  confFile = getConfig()
  authString = base64.encodestring('%s:%s' % (confFile['config']['user'], confFile['config']['pass'])).replace('\n', '')
  authString = "Basic "+authString

  headers = {'Authorization': authString,
    'Content-Type' : 'application/json'}
  url = confFile['config']['url']+"search?jql="+args.query
  r = requests.get(url, headers=headers)
  print r.text

def getConfig():
  if (os.path.isfile("config.json")):
    with open("config.json") as confFile:
      confFile = json.load(confFile)
  else:
    print("Can't find config.json")
    sys.exit(1)
  return confFile

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Jira API test")
  subparsers = parser.add_subparsers()

  parser_query = subparsers.add_parser('query')
  parser_query.add_argument('-q','--query',required=True)
  parser_query.set_defaults(func=doQuery)

  args = parser.parse_args()
  args.func(args)

  sys.exit(0)
  
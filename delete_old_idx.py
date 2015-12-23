#!/usr/bin/python
import requests
import argparse
import json
import re
from datetime import date, timedelta
import datetime
# argument check
parser = argparse.ArgumentParser(description='Delete Elasticsearch Old Indices')
parser.add_argument('host', metavar='HOSTNAME', type=str, help='Elsticsearch Host name or IP')
parser.add_argument('days', metavar='DAYS', type=int, help='Days to keep indices')
parser.add_argument('-prefix', type=str, help='Index prefix to delete')

args = parser.parse_args()

res = requests.get('http://'+args.host+':9200')

if res.status_code != 200 :
	print "Couldn't get Elasticsearch info"
	sys.exit()

res = requests.get('http://'+args.host+':9200/_all/_settings')
r = res.json()

for key, val in r.iteritems():
	k = key.split("_", 1)
	
	if k[1] is None:
		continue
	
	idx_date = k[1].replace("\W","")
	
	if idx_date.isdigit() is False:
		continue
	
	if args.prefix is not None:
		if k[0] != args.prefix:
			continue
	if datetime.datetime.strptime(idx_date, "%Y%m%d").date() == (date.today() - timedelta(args.days)):
		d = requests.delete('http://'+args.host+':9200/' + key)
		if d.status_code != 200 :
			print "Fail to delete index:", key
		else:
			print "Delete", key, "successfully" 

#!/usr/bin/env python3
# Callsign searcher for Hungarian (HA/HG) callsigns
# Takes a pattern, and returns the number of callsigns matching the query
# Powered by HA5KDR's callsign searcher
# Written by CsokiCraft (HA7CSK), 2022
# Licensed under WTFPL

import requests
import sys

if len(sys.argv) != 2:
	print("Usage: {} <callsign>".format(sys.argv[0]))
	sys.exit(1)

params = (
	('jtStartIndex', '0'),
	('jtPageSize', '10'),
	('jtSorting', 'validity ASC'),
)

data = {
	'searchfor': sys.argv[1]
}

response = requests.post('https://www.ha5kdr.hu/wp-content/plugins/ha5kdr-csb/ha5kdr-csb-getdata.php', params=params, data=data)
print(response.json()["TotalRecordCount"])

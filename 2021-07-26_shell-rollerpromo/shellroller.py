#!/usr/bin/env python3

"""
Shell-Ferrari roller promo batch uploader
"""

import requests
import sys

# document.getElementsByName("user_id")[0].value
user_id = '5821'

headers = {
	'Content-Type': 'application/x-www-form-urlencoded',
	'Origin': 'https://rollerpromo.hu',
}

data = [
	('user_id', user_id)
]

for c in sys.argv[1].upper():
	data.append(('ssn[]', c))

response = requests.post('https://api.rollerpromo.hu/upload', headers=headers, data=data, allow_redirects=False)

print(response.headers["Location"])

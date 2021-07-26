# Mattermost csatorna kexporter v1.0
# (c) 2020 by Csoki
# Licensz: AGPL 3.0 vagy újabb
# RIP agocsdaniel/danca

import requests, json, base64, sys, gzip
from mmcreds import MMAUTHTOKEN

p=0
order=[]
posts={}
emoji_ids=set()
file_ids=set()

SCHNIX="44ifzscrp7yfjg6spstspjdscr"

cookies = {
	'MMAUTHTOKEN': MMAUTHTOKEN,
	'Pragma': 'no-cache'
}

headers = {
	'Connection': 'keep-alive',
	'Cache-Control': 'no-cache',
	'Pragma': 'no-cache',
}

print("Grabbing posts")
while True:
	params = (
		('page', p),
		('per_page', '200'),
		('skipFetchThreads', 'false'),
	)

	response = requests.get('https://mattermost.kszk.bme.hu/api/v4/channels/'+SCHNIX+'/posts', headers=headers, params=params, cookies=cookies)
	if response.status_code != 200:
		print("HTTP Error", response.status_code, "on page", p)
	obj = response.json()

	if not obj["order"]:
		break

	order+=obj["order"]
	for k in obj["posts"].keys():
		posts[k]=obj["posts"][k]

		if "metadata" in posts[k] and "emojis" in posts[k]["metadata"]:
			for e in posts[k]["metadata"]["emojis"]:
				emoji_ids.add(e["id"])

		if "file_ids" in posts[k]:
			for e in posts[k]["file_ids"]:
				file_ids.add(e)

	print('page', p, 'had', len(order), 'posts')
	p+=1

print("Retrieving users")
params = (
	('in_channel', SCHNIX),
)
response = requests.get('https://mattermost.kszk.bme.hu/api/v4/users', headers=headers, params=params, cookies=cookies)
if response.status_code != 200:
	print("HTTP Error", response.status_code, "looking up users")
users=response.json()

print("Saving", len(emoji_ids), "emojis")
emojis={}
for eid in emoji_ids:
	response = requests.get('https://mattermost.kszk.bme.hu/api/v4/emoji/'+eid+'/image', headers=headers, params=params, cookies=cookies)
	if response.status_code != 200:
		print("HTTP Error", response.status_code, "for emoji", eid)
	emojis[eid]=base64.b64encode(response.content).decode()
	perc=len(emojis)/len(emoji_ids)*100
	sys.stdout.write("{:.1f}".format(perc)+"%\x1b[G")
	sys.stdout.flush()

print("Saving", len(file_ids), "files")
files={}
for fid in file_ids:
	response = requests.get('https://mattermost.kszk.bme.hu/api/v4/files/'+fid, headers=headers, params=params, cookies=cookies)
	if response.status_code != 200:
		print("HTTP Error", response.status_code, "for file", fid)
	files[fid]=base64.b64encode(response.content).decode()
	perc=len(files)/len(file_ids)*100
	sys.stdout.write("{:.1f}".format(perc)+"%\x1b[G")
	sys.stdout.flush()

print("Writing to disk, please do not umount / ...")
with gzip.open("/tmp/schnix.json.gz", "wt") as f:
	json.dump({"posts": posts, "order": order, "users": users, "emojis": emojis, "files": files}, f, indent=1)

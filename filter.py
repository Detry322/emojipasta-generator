import json, glob

FILES = glob.glob('download/*/*/*/*.json')

good = {}

dups = 0
total = 0

for f in FILES:
  with open(f, 'r') as fi:
    j = json.load(fi)
    for post in j['data']['children']:
      i = post['data']['id']
      if i == '4hsh42':
        continue
      if i not in good:
        good[i] = post

with open('posts.json', 'w') as f:
  f.write(json.dumps(good, indent=4, separators=(',', ': ')))

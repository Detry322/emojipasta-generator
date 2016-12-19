BASE_URL = 'https://www.reddit.com/r/emojipasta/top.json?sort=top&t=all'

USER_AGENT = 'emojipasta downloader by /u/jserrino'

import requests
import random
import string
import os
from hashlib import sha256

def _hash(text):
  s = sha256()
  s.update(text)
  return s.hexdigest()

def download_after(after):
  url = BASE_URL
  if after:
    url += '&after=' + after
  r = requests.get(url, headers={'User-Agent': USER_AGENT})
  filename = _hash(r.text)
  directory = 'download/{}/{}/{}'.format(*filename[:3])
  if not os.path.exists(directory):
    os.makedirs(directory)
  with open('{}/{}.json'.format(directory, filename), 'w') as f:
    f.write(r.text)
  json = r.json()
  return json['data']['after'], len(json['data']['children'])

a = None
while True:
  a, count = download_after(a)
  print "Downloaded {}".format(count)

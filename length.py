import json
from uniseg.graphemecluster import grapheme_clusters

with open('posts.json', 'r') as f:
  data = json.load(f)

total = 0
grapheme_total = 0

for _, post in data.iteritems():
  grapheme_total += len(list(grapheme_clusters(post['data']['selftext'])))
  grapheme_total += len(list(grapheme_clusters(post['data']['title'])))
  total += len(post['data']['selftext'])
  total += len(post['data']['title'])

print total, grapheme_total

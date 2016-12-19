import json
from uniseg.graphemecluster import grapheme_clusters

with open('posts.json', 'r') as f:
  data = json.load(f)

clusters = set([])

for _, post in data.iteritems():
  clusters.update(grapheme_clusters(post['data']['selftext']))
  clusters.update(grapheme_clusters(post['data']['title']))

for cluster in clusters:
  print cluster.__repr__(),
  print ': ',
  print cluster

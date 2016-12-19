import json, random
import numpy as np
from uniseg.graphemecluster import grapheme_clusters

START_CHAR = u'###START### '
STOP_CHAR = u' ###STOP##'

AMOUNT_TRAIN = 10

def get_sentences():
  sentences = []
  with open('posts.json', 'r') as f:
    data = json.load(f)
    for _, post in data.iteritems():
      sentences.append(post['data']['title'])
      sentences.append(post['data']['selftext'])
  return filter(lambda x: 10 <= len(x) <= 2000, sentences)

def split_sentence(sentence):
  clusters = grapheme_clusters(sentence)
  return [cluster for cluster in clusters if len(cluster) <= 4]

def characters(split_sentences):
  characters = set([])
  for sentence in split_sentences:
    characters.update(sentence)
  character_dict = dict((c, i + 1) for i, c in enumerate(characters))
  character_dict[START_CHAR] = len(characters) + 1
  character_dict[STOP_CHAR] = len(characters) + 2
  reverse_char_dict = [u''] + [character for character, _ in sorted(list(character_dict.iteritems()), key=lambda (c, i): i)]
  return character_dict, reverse_char_dict

def transpose(data):
  result = zip(*data)
  return np.array(result[0]), np.array(result[1])

def create_dataset_generator(split_sentences, cdata, max_len):
  character_dict, reverse_char_dict = cdata
  while True:
    for sentence in enumerate(split_sentences):
      data = []
      for i in range(len(sentence) + 1):
        answer = STOP_CHAR if i == len(sentence) else sentence[i]
        answer_array = [0]*len(reverse_char_dict)
        answer_array[character_dict[answer]] = 1
        question = [character_dict[START_CHAR]]
        question.extend((character_dict[c] if c in character_dict else -1) for c in sentence[:i])
        question.extend([0]*max_len)
        question = question[:max_len + 2]
        data.append((np.array(question), np.array(answer_array)))
      yield transpose(data)

def dataset_length(split_sentences):
  total = 0
  for sentence in split_sentences:
    total += len(sentence) + 1
  return total

def dataset_generator_factory(split_sentences, cdata, max_len):
  generator = create_dataset_generator(split_sentences, cdata, max_len)
  return generator, dataset_length(split_sentences)

def get_data():
  print "Getting sentences..."
  sentences = get_sentences()
  print "Splitting sentences..."
  split_sentences = [split_sentence(sentence) for sentence in sentences]
  max_len = max(len(s) for s in split_sentences)
  print "Creating character mappings..."
  cdata = characters(split_sentences)
  print "Creating dataset..."
  random.shuffle(split_sentences)
  print "Creating train/validate sets..."
  train_sentences, validate_sentences = split_sentences[len(split_sentences)/AMOUNT_TRAIN:], split_sentences[:len(split_sentences)/AMOUNT_TRAIN]
  train = dataset_generator_factory(train_sentences, cdata, max_len)
  validate = dataset_generator_factory(validate_sentences, cdata, max_len)
  return train, validate, max_len, cdata

if __name__ == "__main__":
  print get_data()

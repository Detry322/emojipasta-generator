from keras.models import Sequential
from keras.layers import Dense, LSTM, Masking, Dropout, Embedding, TimeDistributed

import numpy as np

from data import get_data, START_CHAR, STOP_CHAR

MAX_GENERATED = 2000

def get_model(length, reverse_char_dict):
  model = Sequential()
  model.add(Embedding(len(reverse_char_dict) + 1, 50, mask_zero=True, input_length=length))
  model.add(LSTM(100, return_sequences=True))
  model.add(TimeDistributed(Dropout(0.2)))
  model.add(TimeDistributed(Dense(100)))
  model.add(LSTM(100, return_sequences=True))
  model.add(TimeDistributed(Dropout(0.2)))
  model.add(TimeDistributed(Dense(100)))
  model.add(LSTM(100))
  model.add(Dense(100))
  model.add(Dense(len(reverse_char_dict), activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  return model

def train_model(model, train, validate):
  model.fit_generator(
    generator=train[0],
    samples_per_epoch=train[1],
    nb_epoch=100,
    validation_data=validate[0],
    nb_val_samples=validate[1]
  )

def get_prediction(class_probabilities):
  return list(class_probabilities).index(max(class_probabilities))

def generate_sentence(model, length, cdata):
  input_data = np.zeros(length)
  input_data[0] = cdata[0][START_CHAR]
  index = 1
  while index < length:
    result = model.predict_proba(np.array([input_data]))[0]
    prediction = get_prediction(result)
    input_data[index] = prediction
    index += 1
    if prediction == cdata[0][STOP_CHAR]:
      break
  sentence = u''
  for val in input_data:
    sentence += cdata[1][val]
  return sentence

if __name__ == '__main__':
  train, validate, max_len, cdata = get_data()
  model = get_model(max_len, cdata[1])
  train_model(model, train, validate)
  print generate_sentence(model, max_len, cdata)

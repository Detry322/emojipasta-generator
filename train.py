from keras.models import Sequential
from keras.layers import Dense, LSTM, Masking, Dropout, Embedding, TimeDistributed
from keras.callbacks import ModelCheckpoint, LambdaCallback

import numpy as np

from data import get_data, START_CHAR, STOP_CHAR, CONTEXT_LENGTH

MAX_GENERATED = 2000

def get_model(length, reverse_char_dict):
  model = Sequential()
  model.add(Embedding(len(reverse_char_dict) + 1, 64, mask_zero=True, input_length=length))
  model.add(LSTM(128))
  model.add(Dense(64))
  model.add(Dropout(0.2))
  model.add(Dense(len(reverse_char_dict), activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  return model

def train_model(model, train, validate, max_len, cdata):
  def on_epoch_end(epoch, logs):
    with open('{}.txt'.format(epoch), 'w') as fi:
      fi.write(generate_sentence(model, max_len, cdata).encode('utf8'))

  model.fit_generator(
    generator=train[0],
    samples_per_epoch=train[1],
    nb_epoch=1000,
    validation_data=validate[0],
    nb_val_samples=validate[1],
    callbacks=[ModelCheckpoint('model.h5'), LambdaCallback(on_epoch_end=on_epoch_end)]
  )

def get_prediction(class_probabilities):
  return list(class_probabilities).index(max(class_probabilities))

def generate_sentence(model, length, cdata):
  prediction = cdata[0][START_CHAR]
  last_input = np.zeros(CONTEXT_LENGTH)
  results = [prediction]
  while prediction != cdata[0][STOP_CHAR] and len(results) < MAX_GENERATED:
    first_zero = next((i for i, value in enumerate(last_input) if value == 0), None)
    if first_zero is not None:
      input_data = last_input
      input_data[first_zero] = prediction
    else:
      input_data = np.zeros(CONTEXT_LENGTH)
      input_data[CONTEXT_LENGTH-1] = prediction
      for i in range(1, CONTEXT_LENGTH):
        input_data[i-1] = last_input[i]
    result = model.predict_proba(np.array([input_data]))[0]
    prediction = get_prediction(result)
    results.append(prediction)
    last_input = input_data

  sentence = u''
  for val in results:
    sentence += cdata[1][int(val)]
  print sentence
  return sentence

if __name__ == '__main__':
  train, validate, max_len, cdata = get_data()
  print "Creating model..."
  model = get_model(max_len, cdata[1])
  print "Training model..."
  train_model(model, train, validate, max_len, cdata)

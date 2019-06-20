from __future__ import absolute_import, division, print_function

import tensorflow as tf
from tensorflow import keras
import numpy as np

class TFPredictor():
    imdb = keras.datasets.imdb
    word_index = imdb.get_word_index()
    model = keras.Sequential()
    
    def __init__(self, epochs):
        print(tf.__version__)


        (train_data, train_labels), (test_data, test_labels) = self.imdb.load_data(num_words=10000)        

        # The first indices are reserved
        self.word_index = {k:(v+3) for k,v in self.word_index.items()} 
        self.word_index["<PAD>"] = 0
        self.word_index["<START>"] = 1
        self.word_index["<UNK>"] = 2  # unknown
        self.word_index["<UNUSED>"] = 3

        train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                                value=self.word_index["<PAD>"],
                                                                padding='post',
                                                                maxlen=256)

        # input shape is the vocabulary count used for the movie reviews (10,000 words)
        vocab_size = 10000

        
        self.model.add(keras.layers.Embedding(vocab_size, 16))
        self.model.add(keras.layers.GlobalAveragePooling1D())
        self.model.add(keras.layers.Dense(16, activation=tf.nn.relu))
        self.model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

        #self.model.summary()

        self.model.compile(optimizer='adam',
                    loss='binary_crossentropy',
                    metrics=['acc'])

        x_val = train_data[:10000]
        partial_x_train = train_data[10000:]

        y_val = train_labels[:10000]
        partial_y_train = train_labels[10000:]

        self.model.fit(partial_x_train,
                            partial_y_train,
                            epochs=epochs,
                            batch_size=512,
                            validation_data=(x_val, y_val),
                            verbose=1)

    def predict(self, message):
        test = []
        for word in message:
            test.append(self.word_index[word])
        test = keras.preprocessing.sequence.pad_sequences([test],maxlen=256)
        return "%0.5f"%self.model.predict(test)[0][0]
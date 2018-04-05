import helper
from helper import imageToarray , makeDataAndLabels , makePickle

import configure as conf

data , labels , file_names = makeDataAndLabels(dataset=conf.dataset, tag=conf.tag, sizeX=conf.sizeX , sizeY=conf.sizeY)

from sklearn.model_selection import train_test_split

(train1X, test1X, train1Y, test1Y) = train_test_split(data, labels, test_size=0.30, random_state=42)
(train2X, test2X, train2Y, test2Y) = train_test_split(train1X, train1Y, test_size=0.20, random_state=42)
(train3X, test3X, train3Y, test3Y) = train_test_split(train2X, train2Y, test_size=0.50, random_state=42)


#import deepdish as dd
import numpy as np
import h5py
data_file_1 = h5py.File('./h5s/dataset1.hdf5', 'w')
data_file_1.create_dataset('dataset1', data=(train1X, test1X, train1Y, test1Y))
data_file_1.close()
data_file_2 = h5py.File('./h5s/dataset2.hdf5', 'w')
data_file_2.create_dataset('dataset2', data=(train2X, test2X, train2Y, test2Y))
data_file_2.close()
data_file_3 = h5py.File('./h5s/dataset3.hdf5', 'w')
data_file_3.create_dataset('dataset3', data=(train3X, test3X, train3Y, test3Y))
data_file_3.close()

#dd.io.save('./h5s/dataset1.h5', {'trainx':train1X, 'testx':test1X, 'trainy':train1Y, 'testy':test1Y})
#dd.io.save('./h5s/dataset2.h5', {'trainx':train2X, 'testx':test2X, 'trainy':train2Y, 'testy':test2Y})
#dd.io.save('./h5s/dataset3.h5', {'trainx':train3X, 'testx':test3X, 'trainy':train3Y, 'testy':test3Y})

#makePickle(data = data , labels = labels, file_names = file_names ,pickle_path = conf.pickle_path)

import helper
from helper import imageToarray , makeDataAndLabels , makePickle

import configure as conf

data , labels , file_names = makeDataAndLabels(dataset=conf.dataset, tag=conf.tag, sizeX=conf.sizeX , sizeY=conf.sizeY)

makePickle(data = data , labels = labels, file_names = file_names ,pickle_path = conf.pickle_path)

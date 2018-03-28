import helper
from helper import imageToarray , makeDataAndLabels , makePickle

import configure as conf

data , labels = makeDataAndLabels(dataset=conf.dataset, tag=conf.tag, sizeX=conf.sizeX , sizeY=conf.sizeY)
makePickle(data = data , labels = labels, pickle_path=conf.pickle_path)

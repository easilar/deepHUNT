import helper
from helper import imageToarray , makeDataAndLabels , makePickle

import configure as conf

data , labels = makeDataAndLabels(conf.dataset, conf.tag, sizeX=conf.sizeX , sizeY=conf.sizeY)
makePickle(data , labels, conf.pickle_path)

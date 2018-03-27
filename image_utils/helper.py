import matplotlib
import os , sys

import keras
from keras.preprocessing.image import img_to_array
from imutils import paths
import random
import numpy as np
import cv2

import pickle


def imageToarray(imagePath, sizeX, sizeY):
	image = cv2.imread(imagePath)
        print "image will be resized:" , sizeX , sizeY
	image = cv2.resize(image, (sizeX, sizeY))
	image = img_to_array(image)
        return image

def makeDataAndLabels(dataset, tag , sizeX , sizeY):

    data = []
    labels = []

    # grab the image paths and randomly shuffle them
    imagePaths = sorted(list(paths.list_images(dataset)))
    random.seed(42)
    random.shuffle(imagePaths)

    for imagePath in imagePaths:
	# load the image, pre-process it, and store it in the data list
        print "image path:" , imagePath
	image = imageToarray(imagePath, sizeX, sizeY)
        data.append(image)

	# extract the class label from the image path and update the labels
	label = imagePath.split(os.path.sep)[-2]
        print "label 1:" , label
	label = 1 if label == tag else 0
        print "label 2:" , label
	labels.append(label)

    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)

    return data , labels

def makePickle(data , labels, pickle_path):
	dLs_dict = {}
	dLs_dict["data"] = data
	dLs_dict["labels"] = labels
	pickle.dump(dLs_dict,file(pickle_path,'w'))
	return

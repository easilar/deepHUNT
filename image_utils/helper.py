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
        #print "image will be resized:" , sizeX , sizeY
	image = cv2.resize(image, (sizeX, sizeY))
	image = img_to_array(image) #dtype=uint8 -> dtype=float32
        return image

def makeDataAndLabels(dataset, tag , sizeX , sizeY, splitFac):
	print 'now in makeDataAndLabels'
	data = []
	labels = []
	file_names = []
	# grab the image paths and randomly shuffle them
	imagePaths = sorted(list(paths.list_images(dataset)))
	#imagePaths = sorted([os.path.join(dataset, f) for f in os.listdir(dataset)])
	#print 'will be used these image paths:', imagePaths
	random.seed(42)
	random.shuffle(imagePaths)

	datasets = {}

	if splitFac:
	    datasets['val_block']   = {'imagepaths':imagePaths[int(len(imagePaths)*(1-splitFac[0])):]}
	    datasets['test_block']  = {'imagepaths':imagePaths[:int(len(imagePaths)*(1-splitFac[0]))]}
	    datasets['train_block'] = {'imagepaths':datasets['test_block']['imagepaths'][int(len(datasets['test_block']['imagepaths'])*(1-splitFac[1])):]}
	    print len(datasets['val_block']) , len(datasets['test_block']) , len(datasets['train_block']) 
	else: datasets['orig'] = imagePaths

	for dataset in datasets: 
		print 'processing images for :' , dataset
		for imagePath in datasets[dataset]['imagepaths']:
			# load the image, pre-process it, and store it in the data list
			#print "image path:" , imagePath
			image = imageToarray(imagePath, sizeX, sizeY)
			data.append(image)
			file_name = imagePath.split('/')[4]
			#print 'file_name' , file_name
			file_names.append(file_name)
			# extract the class label from the image path and update the labels
			label = imagePath.split(os.path.sep)[-2]
			#print "label 1:" , label
			label = 1 if label == tag else 0
			#print "label 2:" , label
			labels.append(label)

		#data = np.array(data, dtype="float32") / 255.0
		datasets[dataset]['data'] = np.array(data) / 255.0
		datasets[dataset]['labels'] = np.array(labels)
		datasets[dataset]['file_names'] = file_names

	return datasets
	
def makePickle(data , labels, file_names , pickle_path):
	dLs_dict = {}
	dLs_dict["data"] = data
	dLs_dict["labels"] = labels
	dLs_dict["file_names"] = file_names
	pickle.dump(dLs_dict,file(pickle_path,'w'))
	return

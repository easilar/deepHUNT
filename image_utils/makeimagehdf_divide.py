import helper
from helper import imageToarray , makeDataAndLabels , makePickle , list_images
import matplotlib
import os , sys

import random
import numpy as np
import cv2
import h5py

import pickle


import configure as conf

dataset=conf.dataset
imagePaths = sorted(list(list_images(dataset)))
random.seed(42)
random.shuffle(imagePaths)


splitFac=(0.1,0.1,0.3)

datasets = {}

datasets['val1_block']   = {'imagepaths':imagePaths[int(len(imagePaths)*(1-splitFac[0])):]}

rest_block  = imagePaths[:int(len(imagePaths)*(1-splitFac[0]))]

datasets['val2_block']  = {'imagepaths':rest_block[int(len(rest_block)*(1-splitFac[1])):]}

rest2_block  = rest_block[:int(len(rest_block)*(1-splitFac[1]))]

datasets['test_block']  = {'imagepaths':rest2_block[int(len(rest2_block)*(1-splitFac[2])):]}
datasets['train_block'] = {'imagepaths':rest2_block[:int(len(rest2_block)*(1-splitFac[2]))]}

print(len(datasets['val1_block']['imagepaths']), len(datasets['val2_block']['imagepaths']) , len(datasets['test_block']['imagepaths']) , len(datasets['train_block']['imagepaths']))

for key in datasets.keys():
	print('processeing images for :' , key)
	(data , labels , file_names) = makeDataAndLabels(datasets[key]['imagepaths'], tag=conf.tag, sizeX=conf.sizeX , sizeY=conf.sizeY )	
	datasets[key]['data'] = data
	datasets[key]['labels'] = labels

test_block =datasets["test_block"]
train_block=datasets["train_block"]
val1_block =datasets["val1_block"]
val2_block =datasets["val2_block"]


data_file_1 = h5py.File(conf.test_train, 'w')
print('Saving train/test ...')
data_file_1.create_dataset('trainX',data=train_block['data'])
data_file_1.create_dataset('trainY',data=train_block['labels'])
data_file_1.create_dataset('testX',data=test_block['data'])
data_file_1.create_dataset('testY',data=test_block['labels'])
data_file_1.close()

data_file_2 = h5py.File(conf.validations, 'w')
print('Saving Validation ...')
data_file_2.create_dataset('val1_X',data=val1_block['data'])
data_file_2.create_dataset('val1_Y',data=val1_block['labels'])
data_file_2.create_dataset('val2_X',data=val2_block['data'])
data_file_2.create_dataset('val2_Y',data=val2_block['labels'])
data_file_2.close()


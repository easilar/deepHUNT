# USAGE
# python train_network.py

# set the matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use("Agg")

# import the necessary packages
from keras.optimizers import Adam
from keras.callbacks import TensorBoard
from keras import metrics
from keras.preprocessing.image import ImageDataGenerator , img_to_array
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from deepHunt import deepHunt
from metric_helper import precision , sensitivity, specificity, accuracy, bal_acc, fpr, fnr, fmeasure, mcc, youden, AUC, gmean
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import cv2
import os
import time

import pickle
from ploting_helper import Plot_lossAccuracy
from helper import imageToarray

import configure as conf

import h5py    

f1 = h5py.File('hdf5/dataset.hdf5','r+')
data , labels = f1['data'][()] , f1['labels'][()]
print len(data) , len(labels)
print type(data) , type(labels)

val_data = data[:28362]
val_labels = labels[:28362]
data_ = data[28362:]
labels_ = labels[28362:]

(trainX, testX, trainY, testY) = train_test_split(data_, labels_, test_size=0.30, random_state=42)

# convert the labels from integers to vectors
trainY = to_categorical(trainY, num_classes=2)
testY = to_categorical(testY, num_classes=2)

# construct the image generator for data augmentation
aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
	height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
	horizontal_flip=True, fill_mode="nearest")

# initialize the model
print("[INFO] compiling model...")
model = deepHunt.build(width=conf.sizeX, height=conf.sizeY, depth=3, classes=2)
opt = Adam(lr=conf.INIT_LR, decay=conf.INIT_LR / conf.EPOCHS) #optimizer

model.compile(loss="binary_crossentropy", optimizer=opt,
	metrics=["accuracy",metrics.mae,metrics.categorical_accuracy,'binary_accuracy',precision , sensitivity, specificity, accuracy, bal_acc, fpr, fnr, fmeasure, mcc, youden, AUC, gmean])

#tbCallBack = callbacks.TensorBoard(log_dir='logs/log_noPh, histogram_freq=0,  
#          write_graph=True, write_images=True)
tensorboard = TensorBoard(log_dir="logs/{}".format(time.time()),histogram_freq=1,write_graph=True)
tensorboard.set_model(model)

# train the network
print("[INFO] training network...")
model.fit_generator(aug.flow(trainX, trainY, batch_size=conf.BS),
	validation_data=(testX, testY),
	steps_per_epoch=len(trainX) // conf.BS,
	epochs=conf.EPOCHS,
	verbose=1,
	callbacks=[tensorboard])


# save the model to disk
print("[INFO] serializing network...")
model.save(conf.models_dir+"/"+conf.tag+"no"+conf.tag+str(conf.sizeX)+"noPh.model")

# plot the training loss and accuracy
#plots =[\
#	{"label":"train_loss", "n":conf.EPOCHS ,"plot":H.history["loss"]      ,"color":"r"},
#	{"label":"val_loss"  , "n":conf.EPOCHS ,"plot":H.history["val_loss"]  ,"color":"g"},
#	{"label":"train_acc" , "n":conf.EPOCHS ,"plot":H.history["acc"]       ,"color":"b"},
#	{"label":"val_acc"   , "n":conf.EPOCHS ,"plot":H.history["val_acc"]   ,"color":"c"},
#	]
#
#Plot_lossAccuracy( plots , conf.tag , conf.plot)


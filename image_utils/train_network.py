# USAGE
# python train_network.py

# set the matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use("Agg")

# import the necessary packages
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from lenet import LeNet
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import cv2
import os

import pickle
from ploting_helper import Plot_lossAccuracy
from helper import imageToarray

import configure as conf

data_and_labels_dict = pickle.load(file(conf.pickle_path))
data , labels = data_and_labels_dict["data"] , data_and_labels_dict["labels"] 
print len(data) , len(labels)

# partition the data into training and testing splits using 75% of
# the data for training and the remaining 25% for testing
(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.30, random_state=42)

# convert the labels from integers to vectors
trainY = to_categorical(trainY, num_classes=2)
testY = to_categorical(testY, num_classes=2)

# construct the image generator for data augmentation
aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
	height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
	horizontal_flip=True, fill_mode="nearest")

# initialize the model
print("[INFO] compiling model...")
model = LeNet.build(width=conf.sizeX, height=conf.sizeY, depth=3, classes=2)
opt = Adam(lr=conf.INIT_LR, decay=conf.INIT_LR / conf.EPOCHS) #optimizer
model.compile(loss="binary_crossentropy", optimizer=opt,
	metrics=["accuracy"])

# train the network
print("[INFO] training network...")
H = model.fit_generator(aug.flow(trainX, trainY, batch_size=conf.BS),
	validation_data=(testX, testY), steps_per_epoch=len(trainX) // conf.BS,
	epochs=conf.EPOCHS, verbose=1)

# save the model to disk
print("[INFO] serializing network...")
model.save(conf.models_dir+"/"+conf.tag+"no"+conf.tag+str(conf.sizeX)+".model")

# plot the training loss and accuracy
plots =[\
        {"label":"train_loss", "n":conf.EPOCHS ,"plot":H.history["loss"]      ,"color":"r"},
        {"label":"val_loss"  , "n":conf.EPOCHS ,"plot":H.history["val_loss"]  ,"color":"g"},
        {"label":"train_acc" , "n":conf.EPOCHS ,"plot":H.history["acc"]       ,"color":"b"},
        {"label":"val_acc"   , "n":conf.EPOCHS ,"plot":H.history["val_acc"]   ,"color":"c"},
        ]

Plot_lossAccuracy( plots , conf.tag , conf.plot)


import configure as conf

from load_images import get_data_from_hdf5

data_ = get_data_from_hdf5(conf.test_train)

print('obtaining data from hdf5 file, this my take 5 min...')
data_.get_data()

#For labels: get a binary matrix representation of the input.
import useful_fromKeras as k_moduls 
data_.trainY = k_moduls.to_categorical(data_.trainY, num_classes=2)
data_.testY = k_moduls.to_categorical(data_.testY, num_classes=2)

import tensorflow as tf
ImageDataGenerator =  tf.keras.preprocessing.image.ImageDataGenerator
# construct the image generator for data augmentation
aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
        height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
        horizontal_flip=True, fill_mode="nearest")

#initialize the model
print("[INFO] compiling model...")
from deepHunt import deepHunt
Adam = tf.keras.optimizers.Adam

from metric_helper import precision , sensitivity, specificity, accuracy, bal_acc, fpr, fnr, fmeasure, mcc, youden, AUC , gmean , auc_roc , tp , tn, fp , fn
import time

INIT_LR = conf.INIT_LR
EPOCHS = conf.EPOCHS

#model_save_name = '_'.join([str(nFilt[0]),str(nFilt[1]),str(kernS[0]),str(denseL),str(INIT_LR),str(EPOCHS)])

model_s = deepHunt.build(width=conf.sizeX, height=conf.sizeY, depth=3, classes=2)

print (model_s.summary())

print('now... multi_gpu')
multi_gpu_model = tf.keras.utils.multi_gpu_model
model = multi_gpu_model(model_s, gpus=4)

print('model compile and get metrics')
mae = tf.keras.metrics.mean_absolute_error
categorical_accuracy = tf.keras.metrics.categorical_accuracy
opt = Adam(lr=INIT_LR, decay=INIT_LR/EPOCHS) #optimizer

model.compile(loss="binary_crossentropy", optimizer=opt,
	metrics=["accuracy",tp , tn, fp , fn])


model.fit(data_.trainX, data_.trainY, batch_size = conf.BS, nb_epoch = EPOCHS)


import numpy as np
# Predicting the Test set results
y_pred = model.predict(data_.testX, verbose=2)
y_pred = np.argmax(y_pred, axis=1)
#y_pred = (y_pred > 0.5)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(np.argmax(data_.testY,axis=1), y_pred)
print(cm)

#print('tensorboard stage ... ')
#TensorBoard =  tf.keras.callbacks.TensorBoard
#tensorboard = TensorBoard(log_dir="logs/{}".format(time.time()),histogram_freq=1,write_graph=True)
#tensorboard.set_model(model)
#
## train the network
#print("[INFO] training network...")
#model.fit_generator(aug.flow(data_.trainX, data_.trainY, batch_size=conf.BS),
#	validation_data=(data_.testX, data_.testY),
#	steps_per_epoch=data_.ntrainX // conf.BS,
#	epochs=EPOCHS,
#	verbose=1,
#	callbacks=[tensorboard])

# save the model to disk
#print("[INFO] serializing network...")
#model.save("models_afterfit/"+conf.tag+"no"+conf.tag+str(conf.sizeX)+'_'+model_save_name+"_confGen_multiGPU.h5")
#model.save_weights("models_afterfit/weights"+conf.tag+"no"+conf.tag+str(conf.sizeX)+'_'+model_save_name+"_confGen_multiGPU.h5")

#model.save("models_afterfit/"+conf.tag+"no"+conf.tag+str(conf.sizeX)+model_save_name+"_confGen_multiGPU.model")
#tf.keras.models.save_model(model, conf.models_dir+"/"+conf.tag+"no"+conf.tag+str(conf.sizeX)+model_save_name+"_confGen_multiGPU_savemodel.h5")



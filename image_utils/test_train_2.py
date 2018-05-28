import configure as conf

from load_images import get_data_from_hdf5

data_ = get_data_from_hdf5(conf.test_train)
print('obtaining data from hdf5 file, this my take 5 min...')
data_.get_data()

data_val = get_data_from_hdf5(conf.validations)
data_val.get_data()

#For labels: get a binary matrix representation of the input.
import useful_fromKeras as k_moduls 
data_.trainY = k_moduls.to_categorical(data_.trainY, num_classes=2)
data_.testY = k_moduls.to_categorical(data_.testY, num_classes=2)
data_val.val1_Y = k_moduls.to_categorical(data_val.val1_Y, num_classes=2)
data_val.val2_Y = k_moduls.to_categorical(data_val.val2_Y, num_classes=2)

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

model_save_name = '_2layer_'

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
	metrics=["accuracy"])


model.fit(data_.trainX, data_.trainY, batch_size = conf.BS, nb_epoch = EPOCHS)


print('tensorboard stage ... ')
TensorBoard =  tf.keras.callbacks.TensorBoard
tensorboard = TensorBoard(log_dir="logs/{}".format(time.time()),histogram_freq=1,write_graph=True)
tensorboard.set_model(model)


# save the model to disk
print("[INFO] serializing network...")
model.save("models_afterfit/"+conf.tag+"no"+conf.tag+str(conf.sizeX)+'_'+model_save_name+"_confGen_multiGPU.h5")
model.save_weights("models_afterfit/weights"+conf.tag+"no"+conf.tag+str(conf.sizeX)+'_'+model_save_name+"_confGen_multiGPU.h5")


import numpy as np
from sklearn.metrics import confusion_matrix , matthews_corrcoef , classification_report, roc_curve , auc 

def call_metrics(y_true, y_pred):
	#classification_report = classification_report(y_true, y_pred)
	#print('classification_report:')
	#print(classification_report)
	cm = confusion_matrix(y_true, y_pred)
	print('cm:',cm)
	tn, fp, fn, tp = cm.ravel()
	specificity = tn / (tn+fp)
	sensitivity = tp / (tp+fn)
	print('specificity:' , specificity)
	print('sensitivity:' , sensitivity)
	mcc = matthews_corrcoef(y_true, y_pred)
	print('mcc:' , mcc)
	#fpr, tpr, thresholds = roc_curve(y_true, y_pred, pos_label=2)
	#print('fpr:' , fpr, 'tpr:' , tpr)
	#auc = auc(fpr, tpr)
	#print('auc:' , auc)
	return


print('Evaluation of the model: test region , validation 1 and validation 2 regions ...')

print('Evaluation of the model: test region')
# Predicting the Test set results
y_pred = model.predict(data_.testX, verbose=2)
y_pred = np.argmax(y_pred, axis=1)
y_true = np.argmax(data_.testY,axis=1)

call_metrics(y_true, y_pred)

print('Evaluation of the model: validation 1')

y_pred = model.predict(data_val.val1_X, verbose=2)
y_pred = np.argmax(y_pred, axis=1)
y_true = np.argmax(data_val.val1_Y,axis=1)

call_metrics(y_true, y_pred)

print('Evaluation of the model: validation 2')

y_pred = model.predict(data_val.val2_X, verbose=2)
y_pred = np.argmax(y_pred, axis=1)
y_true = np.argmax(data_val.val2_Y,axis=1)

call_metrics(y_true, y_pred)

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



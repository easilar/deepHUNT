import configure as conf
from metric_helper import precision , sensitivity, specificity, accuracy, bal_acc, fpr, fnr, fmeasure, mcc, youden, AUC , gmean
from load_images import get_data_from_hdf5
import time


#data_ = get_data_from_hdf5(conf.validations)
#print('obtaining validation data from hdf5 file, this my take 5 min...')
#data_.get_data()

data_ = get_data_from_hdf5(conf.test_train)

print('obtaining data from hdf5 file, this my take 5 min...')
data_.get_data()

#For labels: get a binary matrix representation of the input.
import useful_fromKeras as k_moduls 
data_.trainY = k_moduls.to_categorical(data_.trainY, num_classes=2)
data_.testY = k_moduls.to_categorical(data_.testY, num_classes=2)


import tensorflow as tf

metric_dict = {\
		'precision':precision,
		'sensitivity':sensitivity,
		'specificity':specificity,
		'accuracy':accuracy,
		'bal_acc':bal_acc,
		'fpr':fpr,
		'fnr':fnr,
		'fmeasure':fmeasure,
		'mcc':mcc,
		'youden':youden,
		'gmean':gmean,
		}


model = tf.keras.models.load_model('models/toxicnotoxic25610_20_10_100_0.1_50_confGen_multiGPU_savemodel.h5',custom_objects = metric_dict)
print(model.summary())
#load_model.load_weights('models/weights.h5',by_name=False)

print('tensorboard stage ... ')
TensorBoard =  tf.keras.callbacks.TensorBoard
tensorboard = TensorBoard(log_dir="logs/{}".format(time.time()),histogram_freq=1,write_graph=True)
tensorboard.set_model(model)

ImageDataGenerator =  tf.keras.preprocessing.image.ImageDataGenerator
# construct the image generator for data augmentation
aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
        height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
        horizontal_flip=True, fill_mode="nearest")


# train the network
print("[INFO] training network...")
model.fit_generator(aug.flow(data_.trainX, data_.trainY, batch_size=conf.BS),
       validation_data=(data_.testX, data_.testY),
       steps_per_epoch=data_.ntrainX // conf.BS,
       epochs=50,
       verbose=1,
       callbacks=[tensorboard])

#yp = load_model.predict(data_.val1_X)
model.save('models_afterfit/toxicnotoxic25610_20_10_100_0.1_50_confGen_multiGPU_savemodel.h5')
model.save_weights('models_afterfit/weights_toxicnotoxic25610_20_10_100_0.1_50_confGen_multiGPU_savemodel.h5')

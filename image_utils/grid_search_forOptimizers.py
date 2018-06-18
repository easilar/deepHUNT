import configure as conf


from load_images import get_data_from_hdf5

print('obtaining data from hdf5 file, this my take 5 min...')
data_ = get_data_from_hdf5(conf.test_train)
data_.get_data()

data_val = get_data_from_hdf5(conf.validations)
data_val.get_data()

#For labels: get a binary matrix representation of the input.
import useful_fromKeras as k_moduls 
data_.trainY = k_moduls.to_categorical(data_.trainY, num_classes=2)
data_.testY = k_moduls.to_categorical(data_.testY, num_classes=2)
data_val.val1_Y = k_moduls.to_categorical(data_val.val1_Y, num_classes=2)
data_val.val2_Y = k_moduls.to_categorical(data_val.val2_Y, num_classes=2)


INIT_LR = conf.INIT_LR
EPOCHS = conf.EPOCHS
bs = conf.BS

import tensorflow as tf
#initialize the model
print("[INFO] compiling model...")
from deepHunt import deepHunt , deepHunt_3Conv
Adam = tf.keras.optimizers.Adam
Adamax = tf.keras.optimizers.Adamax
Nadam = tf.keras.optimizers.Nadam
Adadelta = tf.keras.optimizers.Adadelta
Adagrad = tf.keras.optimizers.Adagrad
SGD = tf.keras.optimizers.SGD
RMSprop = tf.keras.optimizers.RMSprop

multi_gpu_model = tf.keras.utils.multi_gpu_model

def create_model(optimizer='Adam', width=conf.sizeX, height=conf.sizeY):
	#get model
	model_s = deepHunt.build(width, height, depth=3, classes=2)
	print (model_s.summary())
	#make multi gpu available
	model = multi_gpu_model(model_s, gpus=4)
	#compile model
	model.compile(loss="binary_crossentropy", optimizer=optimizer(), metrics=["accuracy"])
	return model


Noptimizers = ['SGD', 'RMSprop', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam']
optimizers = [SGD, RMSprop, Adagrad, Adadelta, Adam, Adamax, Nadam]

for n,optimizer in enumerate(optimizers):
	model_save_name = 'optAlg_'+Noptimizers[n] 
	model = create_model(optimizer=optimizer)
	model.fit(data_.trainX, data_.trainY, batch_size = conf.BS, nb_epoch = EPOCHS)	
	print("[INFO] serializing network...")
	model.save("models_gridSearch/"+conf.tag+"no"+conf.tag+str(conf.sizeX)+'_'+model_save_name+"_confGen_multiGPU.h5")
	model.save_weights("models_gridSearch/weights"+conf.tag+"no"+conf.tag+str(conf.sizeX)+'_'+model_save_name+"_confGen_multiGPU.h5")





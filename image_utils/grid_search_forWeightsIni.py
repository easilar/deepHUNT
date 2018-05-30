import configure as conf
import os , sys

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

def create_model(init_mode='random_uniform',lr=0.01, momentum=0.9, optimizer='Adam', width=conf.sizeX, height=conf.sizeY):
	#get model
	model_s = deepHunt.build(width, height, depth=3, classes=2, init_mode=init_mode)
	print (model_s.summary())
	#make multi gpu available
	model = multi_gpu_model(model_s, gpus=4)
	#compile model
	model.compile(loss="binary_crossentropy", optimizer=optimizer(lr=lr,rho=momentum), metrics=["accuracy"])
	#model.compile(loss="binary_crossentropy", optimizer=optimizer(lr=lr, decay=lr/10), metrics=["accuracy"])
	return model


#Noptimizers = ['SGD', 'Adadelta', 'Adam', 'Nadam']
Noptimizers = ['Adadelta']
optimizers = [Adadelta]
lrs = [0.8]
momentums = [0.95]

#For SGD
#lrs = [0.001, 0.01, 0.1, 0.2 , 0.3]
#momentums = [0.01, 0.2, 0.4 ,0.6, 0.8 ,0.9]

#For Adadelta
#lrs = [0.01, 0.01, 0.1, 0.5, 0.8 ,1.0]
#momentums = [0.01, 0.2, 0.6, 0.9, 0.95]

#For Nadam
#lrs = [0.001, 0.002, 0.003, 0.01, 0.5]
#momentums = [0.9]

#For Adam
#lrs =  [0.001, 0.002 , 0.1 , 0.3 , 0.5 , 0.9]
#momentums = [0.9]

weights_ini = ['uniform', 'lecun_uniform', 'normal', 'zero', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform']

for n,optimizer in enumerate(optimizers):
	for lr in lrs:
		for momentum in momentums:
			for init_mode in weights_ini: 
				model_save_name = '_'.join(['optAlg'+Noptimizers[n],'lr'+str(lr).replace('.','p'),'mom'+str(momentum).replace('.','p'),'init_mode_'+init_mode])
				model_dir = "models_gridSearch/"+conf.tag+"no"+conf.tag+str(conf.sizeX)+'_'+model_save_name+"_confGen_multiGPU.h5"
				if not os.path.exists(model_dir):
					model = create_model(init_mode=init_mode,optimizer=optimizer,lr=lr, momentum=momentum)
					model.fit(data_.trainX, data_.trainY, batch_size = conf.BS, nb_epoch = EPOCHS)	
					print("[INFO] serializing network...")
					model.save("models_gridSearch/"+conf.tag+"no"+conf.tag+str(conf.sizeX)+'_'+model_save_name+"_confGen_multiGPU.h5")
					model.save_weights("models_gridSearch/weights"+conf.tag+"no"+conf.tag+str(conf.sizeX)+'_'+model_save_name+"_confGen_multiGPU.h5")


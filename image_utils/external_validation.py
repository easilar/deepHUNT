import os , sys
import tensorflow as tf
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


import numpy as np
from sklearn.metrics import confusion_matrix , matthews_corrcoef , classification_report, roc_auc_score
from sklearn.model_selection import cross_val_score

from metric_helper import call_sk_metrics

for file_name in os.listdir('models_gridSearch/'):
	if not file_name.startswith('toxic'): continue
	if not '_act_' in file_name: continue
	if os.path.exists('models_gridSearch_selected/'+file_name): continue
	print(file_name)
	model = tf.keras.models.load_model('models_gridSearch/'+file_name)
	print(model.summary())
	model.load_weights('models_gridSearch/weights'+file_name,by_name=False)

	print('Evaluation of the model: test region , validation 1 and validation 2 regions ...')

	print('Evaluation of the model: test region')
	# Predicting the Test set results
	y_pred = model.predict(data_.testX, verbose=2)
	y_true = np.argmax(data_.testY,axis=1)

	call_sk_metrics(y_true, y_pred)

	print('Evaluation of the model: validation 1')

	y_pred = model.predict(data_val.val1_X, verbose=2)
	y_true = np.argmax(data_val.val1_Y,axis=1)

	call_sk_metrics(y_true, y_pred)

	print('Evaluation of the model: validation 2')

	y_pred = model.predict(data_val.val2_X, verbose=2)
	y_true = np.argmax(data_val.val2_Y,axis=1)

	out_metrics  = call_sk_metrics(y_true, y_pred)

	if out_metrics['sensitivity'] > 0.5 and out_metrics['specificity'] > 0.5 and out_metrics['auc'] > 0.7:
		model.save("models_gridSearch_selected/"+file_name)
		model.save_weights("models_gridSearch_selected/weights"+file_name)


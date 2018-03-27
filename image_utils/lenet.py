# import the necessary packages
import keras
from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras import backend as K

class LeNet:
	@staticmethod
        def build(width, height, depth, classes): #classes : n total of classes we want to recognize
		# initialize the model
		model = Sequential()
		inputShape = (height, width, depth)   # depth 1 for gray scale , 2 for rgb

		# if we are using "channels first", update the input shape
		if K.image_data_format() == "channels_first":
			inputShape = (depth, height, width)

		# first set of CONV => RELU => POOL layers
		model.add(Conv2D(20, (5, 5), padding="same", # 20 convolution filters, each of which are 5x5.
			input_shape=inputShape))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

		# second set of CONV => RELU => POOL layers
		model.add(Conv2D(50, (5, 5), padding="same"))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

		# first (and only) set of FC => RELU layers
		model.add(Flatten()) # flatten it into a single vector
		model.add(Dense(500))
		model.add(Activation("relu"))

		# softmax classifier
		model.add(Dense(classes)) # the number of nodes is equal to the number of classes , which is 2 in my case 
		model.add(Activation("softmax")) #yield the probability for each class.

		# return the constructed network architecture
		return model

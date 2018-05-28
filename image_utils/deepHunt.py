# import the necessary packages
import tensorflow as tf
Sequential = tf.keras.models.Sequential
Conv2D = tf.keras.layers.Convolution2D
MaxPooling2D = tf.keras.layers.MaxPooling2D
Activation = tf.keras.layers.Activation
Flatten = tf.keras.layers.Flatten
Dense = tf.keras.layers.Dense
Dropout = tf.keras.layers.Dropout

class deepHunt:

	@staticmethod

	def build(width, height, depth, classes): 
		#classes : n total of classes we want to recognize
		# initialize the model
		model = Sequential()
		inputShape = (height, width, depth)

		# first set of CONV => RELU => POOL layers
		# n convolutional filters, each of which are mXm 
		model.add(Conv2D(20, kernel_size=(5,5), input_shape=inputShape))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

		model.add(Conv2D(50, kernel_size=(5,5)))
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

class deepHunt_3Conv:

	@staticmethod

	def build(width, height, depth, classes): 
		#classes : n total of classes we want to recognize
		# initialize the model
		model = Sequential()
		inputShape = (height, width, depth)

		# first set of CONV => RELU => POOL layers
		# n convolutional filters, each of which are mXm 
		model.add(Conv2D(20, kernel_size=(5,5), input_shape=inputShape))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

		model.add(Conv2D(30, kernel_size=(5,5)))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

		model.add(Conv2D(50, kernel_size=(5,5)))
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

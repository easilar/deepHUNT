import numpy as np
import cv2
import matplotlib.pyplot as plt

import seaborn as sns
sns.set()

image_path = 'tests/toxic_mol_mol1476_3700_0_45.jpeg'
image = cv2.imread(image_path)
image = cv2.resize(image, (256,256))
#cv2.imwrite('tests/toxic_mol_mol1476_3700_0_45_28t28.jpeg',image)

#print image

# import the necessary packages
import keras
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.models import Sequential

model = Sequential()
model.add(Conv2D(5, (10, 10), padding="same", input_shape=image.shape))
toxic_batch = np.expand_dims(image,axis=0)
conv_toxic = model.predict(toxic_batch)

image = np.squeeze(toxic_batch,axis=0)
print image.shape

plt.figure()
plt.imshow(image)
plt.savefig("tests/toxic_mol_mol1476_3700_0_45_256t256_Conv10b10_filt5.jpeg")



'''
reds = np.array([[image[x][y][0] for y in range(len(image[x]))] for x in range(len(image))])
redax = sns.heatmap(reds)
figR = redax.get_figure()
figR.savefig("tests/toxic_mol_mol1476_3700_0_45_256t256_Reds.jpeg")

greens = np.array([[image[x][y][1] for y in range(len(image[x]))] for x in range(len(image))])
greenax = sns.heatmap(greens)
figG = greenax.get_figure()
figG.savefig("tests/toxic_mol_mol1476_3700_0_45_256t256_Greens.jpeg")
#
blues = np.array([[image[x][y][2] for y in range(len(image[x]))] for x in range(len(image))])
blueax = sns.heatmap(blues)
figB = blueax.get_figure()
figB.savefig("tests/toxic_mol_mol1476_3700_0_45_256t256_Blues.jpeg")
'''




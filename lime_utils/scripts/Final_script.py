#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import cv2
import lime 
import pickle
from lime import lime_image
from lime.wrappers.scikit_image import SegmentationAlgorithm
from skimage.segmentation import mark_boundaries


# In[ ]:



from optparse import OptionParser

oparser = OptionParser()
oparser.add_option('--data', default='Tox21_p53_Test'  , action='store')
oparser.add_option('--model_name', default= '1548952376_0874684' , action='store')
oparser.add_option('--test', default=False , action='store')
(options, oargs) = oparser.parse_args()


# In[ ]:


img_width = 128
img_height = 128
def preprocess_image(image_path):
        image = cv2.imread(image_path)
        image = cv2.resize(image, (img_width, img_height))
        img_to_array = tf.keras.preprocessing.image.img_to_array
        image = img_to_array(image)
        image = np.array(image, dtype="float32") / 255.0
        images = np.expand_dims(image, axis=0)
        return images


# In[ ]:


data = options.data
model_name = options.model_name
testing = options.test
path = '../images/'+data+'/toxic'
#result_path1 = '../images/Tox21_p53_Test/Toxic_results_two_features'
#result_path2 = '../images/Tox21_p53_Test/Tox_results_one_features'
model = tf.keras.models.load_model('../models/model_'+model_name+'.h5')
model.load_weights('../models/weights_'+model_name+'.h5')


result_dict = {}
start = '_ID_'
end = '.jpeg'
f = os.listdir(path)
if testing ==True:
    f = f[:10]
for j,file in enumerate(f):
        print('current loop: ',j )        
        s = file
        ID_mol = s[s.find(start)+1:s.rfind(end)]
        print("current_ID:  ",ID_mol)
        result_dict[ID_mol] = {}
        image_path = os.path.join(path,file) 
        images = preprocess_image(image_path)
        print(images.shape)
        print("..explainer is working ...")
        explainer = lime_image.LimeImageExplainer(verbose =True)
        explanation = explainer.explain_instance(images[0], model.predict, top_labels=2, hide_color=0, num_samples=1000,segmentation_fn = SegmentationAlgorithm('quickshift', kernel_size=1,
                                                    max_dist=200, ratio=0.2,random_seed=42))
        temp, mask = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=False, num_features=1, hide_rest=False)
        a = mark_boundaries(temp , mask)
        print(a.mean())
        result_dict[ID_mol]["num_features_1"] = {} 
        result_dict[ID_mol]["num_features_1"]["temp"] = temp
        result_dict[ID_mol]["num_features_1"]["mask"] = mask
        result_dict[ID_mol]["num_features_1"]["mb"] = a
        result_dict[ID_mol]["num_features_1"]["explanation"] = explanation
        print("..explaination saved ...")
        #temp, mask = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=False, num_features=1, hide_rest=True)
        #plt.imshow(temp)
        
        temp, mask = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=False, num_features=2, hide_rest=False)
        a = mark_boundaries(temp , mask)
        #plt.imshow(a)
        result_dict[ID_mol]["num_features_2"] = {} 
        result_dict[ID_mol]["num_features_2"]["temp"] = temp
        result_dict[ID_mol]["num_features_2"]["mask"] = mask
        result_dict[ID_mol]["num_features_2"]["mb"] = a
        result_dict[ID_mol]["num_features_2"]["explanation"] = explanation
        #temp, mask = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=False, num_features=2, hide_rest=True)
        #regiondetect_twofeature.append(temp)
        #plt.imshow(temp)
        #matplotlib.image.imsave(os.path.join(result_path1+str(file)), a)
        #plt.imshow(mark_boundaries(temp , mask))

if testing == False: 
    f = open('../pickles/results_summary_'+data+model_name+'_pkl','wb')
    pickle.dump(result_dict,f)
    f.close()
    print('file saved as : ' , '../pickles/results_summary_'+data+model_name+'_pkl')
    


# In[ ]:





# In[ ]:





# In[ ]:





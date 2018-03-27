import os , sys
#what to catecorise
tag = "toxic"

#IO
sizeX , sizeY = 28, 28
dataset = "../maestro_utils/images/"
pickle_path = "pickles/data_labels_"+str(sizeX)+"_pkl" 
picle_dir = "pickles"
if not os.path.exists(picle_dir):
      os.makedirs(picle_dir)
models_dir="models"
if not os.path.exists(models_dir):
          os.makedirs(models_dir)

#plotting configuration
plot = "figures/loss_Accuracy_"+str(sizeX) 
plot_dir = "figures/"
if not os.path.exists(plot_dir):
      os.makedirs(plot_dir)

#Configure model

# initialize the number of epochs to train for, initial learning rate,
# and batch size
EPOCHS = 10
INIT_LR = 1e-3
BS = 32


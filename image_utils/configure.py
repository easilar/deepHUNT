import os , sys
#what to catecorise
tag = "toxic"

#original dataset
#dataset_sdf_file = 'sdf_utils/data/Eleni_mulliner_curated_w_ID.sdf' 
dataset_sdf_file = 'sdf_utils/data/ece_cholo.sdf' 
nOrig_toxic = 338
nOrig_nontoxic = 1363
#dataset hdf5
test_train = 'hdf5/train_test.hdf5'
validations = 'hdf5/validations.hdf5'
#IO
sizeX , sizeY = 256, 256
dataset = "../data/Cholo/"
pickle_path = "pickles/data_labels_"+str(sizeX)+"_from"+dataset.split('/')[2]+"_pkl" 
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
BS = 128 #parallel 4x32


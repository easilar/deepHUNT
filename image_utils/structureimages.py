import os
import configure as conf

reverse = True
border = conf.nOrig_toxic + 1
print border 
if reverse: 
	conf.tag = "not_"+conf.tag
	border = conf.nOrig_nontoxic + 1

pathTOstructure = conf.dataset+"/"+conf.tag+"/"
mvpath = "../data/images_noPh_rest/"+conf.tag+"/"
if not os.path.exists(mvpath):
	os.makedirs(mvpath)
print "structuring.... :" , pathTOstructure
for index,filename in enumerate(os.listdir(pathTOstructure)):
        if int(filename.split('_')[4])<border or int(filename.split('_')[5])==-1:
		print filename.split('_')[4] , filename.split('_')[5] ,  border
                print "the file :" , filename
		#os.rename(pathTOstructure+"/"+filename, mvpath+"/"+filename+".jpeg") 
		os.rename(pathTOstructure+"/"+filename, mvpath+"/"+filename) 

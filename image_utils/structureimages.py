import os
import configure as conf

reverse = True
border = conf.nOrig_toxic + 1
if reverse: 
	conf.tag = "not_"+conf.tag
	border = conf.nOrig_nontoxic + 1

pathTOstructure = conf.dataset+"/"+conf.tag+"/"
mvpath = "data/images_noPh_rest/"+conf.tag+"/"
print "structuring.... :" , pathTOstructure
for index,filename in enumerate(os.listdir(pathTOstructure)):
        if int(filename.split('_')[1])<border or int(filename.split('_')[3])==0:
                print "the file :" , filename
		os.rename(pathTOstructure+"/"+filename, mvpath+"/"+filename+".jpeg") 

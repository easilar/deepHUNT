import os
import configure as conf

reverse = True
border = conf.nOrig_toxic + 1
if reverse: 
	conf.tag = "not_"+conf.tag
	border = conf.nOrig_nontoxic + 1

pathTOstructure = conf.dataset+"/"+conf.tag+"/"
print pathTOstructure
#tempdir = conf.dataset+"/"+conf.tag+"/"+conf.tag+"/"
tempdir = '../data/images_noPh_rest/not_toxic/'
for index,filename in enumerate(os.listdir(tempdir)):
	print index , filename 	
	os.rename(tempdir+filename,pathTOstructure+filename.split('.')[0]+'.jpeg')

'''
mvpath = "../data/images_noPh_rest/"+conf.tag+"/"
if not os.path.exists(mvpath):
	os.makedirs(mvpath)
print "structuring.... :" , pathTOstructure
for index,filename in enumerate(os.listdir(pathTOstructure)):
        if int(filename.split('_')[4])<border or int(filename.split('_')[5])==-1:
                print "the file :" , filename
'''

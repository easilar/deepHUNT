import os
import configure as conf


pathTOstructure = "../maestro_utils/images/"+'not'+conf.tag+"/"
print "structuring.... :" , pathTOstructure
for index,filename in enumerate(os.listdir(pathTOstructure)):
	if int(filename.split('_')[1])<1322 or int(filename.split('_')[3])==0: 
		os.remove(pathTOstructure+"/"+filename) 
#os.rename(pathTOstructure+"/"+filename, pathTOstructure+"/"+conf.tag+"_"+str(index)+".jpeg") 

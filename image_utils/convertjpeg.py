import os
import configure as conf


reverses = (False, True)
#reverse = False
for reverse in reverses:
	if reverse: conf.tag = "not_"+conf.tag

	pathTOstructure = "/".join([conf.dataset,conf.tag])
	print "structuring.... :" , pathTOstructure
	for index,filename in enumerate(os.listdir(pathTOstructure)):
		print "the file :" , filename , "will be renamed as ", conf.tag+"_"+filename+".jpeg" 
		os.rename(pathTOstructure+"/"+filename, pathTOstructure+"/"+conf.tag+"_"+filename+".jpeg") 

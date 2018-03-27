import os
import configure as conf

pathTOstructure = "../maestro_utils/images/"+conf.tag+"/"
print "structuring.... :" , pathTOstructure
for index,filename in enumerate(os.listdir(pathTOstructure)):
        if int(filename.split('_')[1])<519 or int(filename.split('_')[3])==0:
                print "the file :" , filename
                os.remove(pathTOstructure+"/"+filename)

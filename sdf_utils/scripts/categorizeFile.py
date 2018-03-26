import os,sys
from sdf_utils.python.helper import *

cur_f = 'sdf_utils/data/Eleni_mulliner_curated_w_ID.sdf'

f1 = readFile(cur_f,printOption=False)

Mols=getMolecules(f1)

data_path = 'sdf_utils/data/categorized/'

cats = ('notoxic','toxic')
for path in cats:
	path = data_path+path
	if not os.path.exists(path): os.makedirs(path)

for index, molText in enumerate(Mols[:-1]):
	mol = molecule(molText[1:],('Inchi_key','Source','ID','H_MFHB','CAS','Cholestasis','Name','Class'))
	print 8*'*'
	print 'class:' , mol.Class , 'index:' , index 
	print 8*'*'
	print mol.content
	ftow = open(data_path+cats[int(mol.Class)]+'/mol'+str(index)+'.sdf','w')
	ftow.write(mol.content+'$$$$')
	ftow.close()

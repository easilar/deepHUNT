import os,sys
from sdf_utils.python.helper import *


from optparse import OptionParser

oparser = OptionParser()
oparser.add_option('--inputpath', default='sdf_utils/data/Eleni_mulliner_curated_w_ID.sdf' , action='store')
oparser.add_option('--outpath', default='sdf_utils/data/categorized/', action='store')
oparser.add_option('--sourceCode', default=0, action='store')
oparser.add_option('--keys', default='ID class', action='store')
(options, oargs) = oparser.parse_args()


cur_f = options.inputpath
data_path = options.outpath
SC = int(options.sourceCode)
keys = options.keys
keys = keys.split(' ')


f1 = readFile(cur_f,printOption=False)

Mols=getMolecules(f1)

folds = ('fold1','fold2','fold3','fold4','fold5')
cats = ('notoxic','toxic')
for fold in folds:
	for path in cats:
		path = '/'.join([data_path,fold,path])
		if not os.path.exists(path): os.makedirs(path)

for index, molText in enumerate(Mols[:-1]):
	#mol = molecule(molText[1:],('Inchi_key','Source','ID','H_MFHB','CAS','Cholestasis','Name','Class'))
	mol = molecule(molText[1:],keys,source_code=SC)
	print(8*'*')
	print('class:' , mol.Class , 'index:' , index)
	print(8*'*')
	print(mol.content)
	ftow = open(data_path+'/fold'+str(mol.Fold)+'/'+cats[int(float(mol.Class))]+'/mol'+str(index)+'.sdf','w')
	ftow.write(mol.content+'$$$$')
	ftow.close()

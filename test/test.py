import os,sys
from sdf_utils.python.helper import *

cur_f = 'sdf_utils/data/Eleni_mulliner_curated_w_ID.sdf'
f1 = readFile(cur_f,printOption=False)
Mols=getMolecules(f1)
len(Mols)
mol_index = 15
Mol = getMoleculeFromIndex(Mols,mol_index)
ftow = open('test/testmol'+str(mol_index)+'.sdf','w')
ftow.write(Mol+'\n$$$$')
ftow.close()




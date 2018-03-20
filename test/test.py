import os,sys
from sdf_utils.python.helper import *

cur_f = 'sdf_utils/data/Eleni_mulliner_curated_w_ID.sdf'
f1 = readFile(cur_f,printOption=False)
Mols=getMolecules(f1)
len(Mols)
Mol = getMoleculeFromIndex(Mols,0)
ftow = open('test/testmol.sdf','w')
ftow.write(Mol+'\n$$$$')
ftow.close()




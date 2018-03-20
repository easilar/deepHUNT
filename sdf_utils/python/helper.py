import os, sys

def readFile(sdffile,printOption=False):
	cur_file = open(sdffile,'r')
	readyfile = cur_file.read()
	if printOption : print 'file is ready to be read'
	return readyfile

def getNmolecules(readyfile, printOption=False):
	count = readyfile.count('$$$$')
	if printOption : print 'number of moleculus :' , count
	return count

def getMolecules(readyfile, printOption=False):
	molecules = readyfile.split('$$$$')
	return molecules

def getMoleculeFromIndex(molecules,index):
	molecule = molecules[index]
	return molecule


class molecule(object):

	def __init__(self, name, ID, Source, H_MFHB, CAS, Cholestasis, classValue, Inchi_key, content):
		self.name = name
		self.ID = ID
		self.Source = Source
		self.H_MFHB = H_MFHB 
		self.CAS = CAS
		self.Cholestasis = Cholestasis
		self.Class = classValue
		self.Inchi_key = Inchi_key
		self.content = content

	def getKeyValuefromMol(self,key):
		return self.content.split('<'+key+'>')[1].split('\n')[1]


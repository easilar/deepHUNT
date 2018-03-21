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

	def __init__(self , content, keys):
		self.content = content
		self.__getKeyValuefromMol(keys)

	def getKeyValuefromMol(self, keys):
		for key in keys:
			keyval = self.content.split('<'+key+'>')[1].split('\n')[1]
			exec('self.'+key+'=keyval')

	__getKeyValuefromMol = getKeyValuefromMol


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

#def createMoleculeDict(molecule):
	

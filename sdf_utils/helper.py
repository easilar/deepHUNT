import os, sys

def getNmolecules(sdffile, printOption=False):
	cur_file = open(sdffile,'r')
	count = cur_file.read().count('$$$$')
	if printOption : print 'number of moleculus found in file' , sdffile, 'is' , count
	return count


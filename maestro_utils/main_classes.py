
#from abc import ABCMeta, abstractmethod

from schrodinger.maestro import maestro
from schrodinger import project
from schrodinger import surface

from helper import *


class engage:

	def __init__(self,name, stages):
		self.name = name
		self.commends = []
		self.__loopOver(stages)

	def loopOver(self,stages):
		for commend in stages:
			self.commends.append(commend)			

	__loopOver = loopOver

class maestroObject(object):

	def __init__(self, name):
		self.name = name

	def rotate(self, angle):
		self.angle = angle
		rotate_by(angle)	

	def getNamefromMakeName(self, prefix , number):
		makeName(self.prefix, self.number)

class virtualRow(maestroObject):

	#__metaclass__  = ABCMeta

	number = -10

	def __init__(self, angle):
		self.angle = angle

	def is_row(self):
		if self.number < 0. :
			raise RuntimeError('Cannot call a row with negative number.')
		return self.number >= 0.

	def includeOnly(self):
		if not self.is_row(): raise RuntimeError('this method can only be used by a row')
		self.includeOnly()

		

class currentRow(virtualRow):

	def __init__(self, proj_tab):
		self.pt = proj_tab

	def makeRow(self):
		self.row = self.pt.getRow(self.number)

class makeSurface(currentRow):
	
	def __init__(self, coloring, style):
		self.color = coloring
		self.style = style
	def createSurf(self):
		self.row.newMolecularSurface(self.name)
		
	def action():
		self.setColoring(self.color)
		self.style(self.style)
	


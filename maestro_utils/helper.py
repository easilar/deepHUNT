import sys,os

from schrodinger.maestro import maestro

def rotate_by(by = 90):
	maestro.command("rotate y=%d" % by)
	return;

def savePng(nrow , angle):
	#Capture the current main structure window and save to an image file.
	maestro.command('saveimage format=%s %s' % ('png', 'MaestroTest/images/test_'+str(nrow)+'_'+str(angle)))
	print 'image saved: ' , 'MaestroTest/images/test_'+str(nrow)+'_'+str(angle)
	return;

def makeName(*args):
	return '_'.join(str(k) for k in args if k is not None)


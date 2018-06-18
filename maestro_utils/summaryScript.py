# add a new molecular surface
# color surface by partial charge
# style set dot
# rotate by 45 degree
# save image as png
import sys,os 
from schrodinger.maestro import maestro
from schrodinger import project
from schrodinger import surface


def rotate_by(by = 90):
	maestro.command("rotate y=%d" % by)

def savePng(inipath):
	#Capture the current main structure window and save to an image file.
	maestro.command('saveimage format=%s %s' % ('jpeg', inipath+'.jpeg'))
	print 'image saved: ' , inipath

def makePath(inipath, name):
	return '/'.join([inipath,name])

def makeName(*args):
	return '_'.join([str(k) for k in args if k is not None])

#get the project table
pt = maestro.project_table_get()
print 'length  of all rows in the project table:' , len(pt.all_rows)

inipath = '/home/ecea/Artemis/deepHunt/data/Muliner/fold1/not_toxic'
if not os.path.exists(inipath):
	os.makedirs(inipath)

coloring = surface.ColorBy.partial_charge
surfStyle = surface.Style.dot
nStep = 7 
angle = 45 # angle for each step
iterable = pt.all_rows
prefix = 'Surf'
generate_surface = False

for row in iterable:
	row.includeOnly()
	title = row.title
	nrow = row.row_number
	print 'number of current row: ' , nrow
	#if nrow < 51:	continue
	save_name = makeName('mol',title,nrow,-1,0)
	fin_path = makePath(inipath, name = save_name)
	savePng(fin_path)
	sName = makeName(prefix, nrow)
	if generate_surface:
		row.newMolecularSurface(sName)
		print 'new surface is name: ', row.surface[sName].name
		surf = row.surface[sName]
		surf.setColoring(coloring)
		surf.style = surface.Style.dot
		maestro.redraw()
	for i in range(nStep):
		rotate_by(angle)
		save_name = makeName('mol',title,nrow,i,angle)
		fin_path = makePath(inipath, name = save_name)
		savePng(fin_path)

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

def savePng(nrow , i=-1, angle=0):
	#Capture the current main structure window and save to an image file.
	maestro.command('saveimage format=%s %s' % ('png', 'images/toxic/mol_'+str(nrow)+'_'+str(i)+'_'+str(angle)))
	print 'image saved: ' , 'images/toxic/mol_'+str(nrow)+'_'+str(i)+'_'+str(angle)

def makeName(*args):
	return '_'.join(str(k) for k in args if k is not None)

#get the project table
pt = maestro.project_table_get()
print 'length  of all rows in the project table:' , len(pt.all_rows)

coloring = surface.ColorBy.partial_charge
surfStyle = surface.Style.dot
nStep = 8 
angle = 45 # angle for each step
iterable = pt.all_rows
prefix = 'Surf'

for row in iterable:
	row.includeOnly()
	nrow = row.row_number
	print 'number of current row: ' , nrow
	savePng(nrow)	
	sName = makeName(prefix, nrow)
	row.newMolecularSurface(sName)
	print 'new surface is name: ', row.surface[sName].name
	surf = row.surface[sName]
	surf.setColoring(coloring)
	surf.style = surface.Style.dot
	#maestro.redraw()
	for i in range(nStep):
		rotate_by(angle)
		savePng(nrow,i,angle)	

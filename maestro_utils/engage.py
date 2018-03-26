from helper import *
from main_classes import *

run_test = True

print '... employing project table'
pt = maestro.project_table_get()

if run_test :

 	ntest = 186
	print '\n'
	print '... test is running' 
	print '... test is running for row number: ' , ntest 
	testrow = currentRow(pt)
	testrow.number = ntest
	testrow.makeRow()
	print '... test row is created' 

	surfcoloring = surface.ColorBy.partial_charge
	surfStyle = surface.Style.dot
	angle = 45 # angle for each step
	prefix = 'Surf'
	
	testsurf = makeSurface(coloring = surfcoloring, style=surfStyle)
	testsurf.row = testrow.row
	testsurf.row.includeOnly()
	print 'surface is added to the row.'
	print 'surface details:'
	print 'coloring: partial_charge'
	print 'style: dot'
	print 'angle: ', angle
	print 'prefix:', prefix 



	


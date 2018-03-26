#when writing Python scripts in which you manipulate an entry in the Workspace, you need to synchronize the Workspace changes with the Project Table before using a Structure entry from the Project Table. 
import sys,os 
from schrodinger.maestro import maestro
from schrodinger import project
from schrodinger import surface

#get the project table
pt = maestro.project_table_get()
print 'length  of all rows in the project table:' , len(pt.all_rows)

#empty lists
all_structures = []
included_structures = []
print 'length  of included structures before addition:' , len(included_structures)
for row in pt.all_rows:
	row.is_selected = True
	included_structures.append(row.getStructure())
	
print 'length  of included structures after addition:' , len(included_structures)
print 'length  of selected structures after addition:' , len(pt.selected_rows)
#maestro.redraw()

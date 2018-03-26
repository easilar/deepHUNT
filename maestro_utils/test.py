import sys,os 
from schrodinger.maestro import maestro
from schrodinger import project
from schrodinger import surface

#surface.Surface.ColorBy.partial_charge
#surface.Style.dot
#setColorsAndSurfacesVisible(True)
#surf.setColoring(surf.ColorBy.atom_color)
pt = maestro.project_table_get()
nrow = 192
exp_row = pt.getRow(nrow)
print exp_row.title
exp_row.newMolecularSurface('MySurf'+str(nrow))
print exp_row.surface['MySurf'+str(nrow)].name


exp_row.surface['MySurf'+str(nrow)].ColorBy.partial_charge
exp_row.surface['MySurf'+str(nrow)].Style.dot
exp_row.surface['MySurf'+str(nrow)]._updateMaestro()
exp_row.surface['MySurf'+str(nrow)].show()

#exp_st = exp_row.getStructure()
#print exp_st.property.keys()

maestro.redraw()
#when writing Python scripts in which you manipulate an entry in the Workspace, you need to synchronize the Workspace changes with the Project Table before using a Structure entry from the Project Table. 
#len(pt.all_rows)
#for row in pt.all_rows:
#	print row
#	st = row.getStructure()
#	print st

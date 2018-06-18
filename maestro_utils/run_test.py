from schrodinger import maestro
pt = maestro.project_table_get()
inipath = '../data/Cholo/toxic'
nStep = 8
angle = 45
iterable = pt.all_rows
for row in iterable:
    row.includeOnly()
    nrow = row.row_number
    print 'number of current row: ' , nrow
    save_name = '_'.join(['mol',str(nrow),str(-1),str(0)])
    fin_path = '/'.join([inipath,save_name])
    maestro.command('saveimage format=%s %s' % ('jpeg', fin_path))
    sName = str(nrow)
    for i in range(nStep):
        maestro.command("rotate y=%d" % angle)
        save_name = '_'.join(['mol',str(nrow),str(i),str(angle)])
        fin_path = '/'.join([inipath,save_name])
        maestro.command('saveimage format=%s %s' % ('jpeg', fin_path))

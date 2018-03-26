$SCHRODINGER/ligprep -bff 16 -epik -s 32 -imae ligprep_1.maegz -omae ligprep_1-out.maegz

Processing steps:
$DO/sdstereoexpander.pyc -max_output 32 -max_generated 1024 <infile.mae> <outfile.mae>
$DO/htreat.pyc -t All-None -a all -s -l 200 <infile.mae> <outfile.mae>
$DO/desalter.pyc <infile.mae> <outfile.mae>
$DO/neutralizer.pyc -m 200 <infile.mae> <outfile.mae>
$DO/epik.pyc -ph 7.0 -tn 8 -ma 200 -imae <infile.mae> -omae <outfile.mae>
$DO/guard.pyc <infile.mae> <outfile.mae>
$DO/stereoizer.pyc -label_specified_chiralities -n 32 <infile.mae> <outfile.mae>
$DO/cgx.pyc -optimize -ffld 16 -epsilon 10.0 <infile.mae> <outfile.mae>

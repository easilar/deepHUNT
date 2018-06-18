# deepHUNT
Hunts toxic compounds

Setup
<br />
```sh
mkdir deepHUNT
cd deepHUNT/
git init
git remote add deepHunt https://github.com/easilar/deepHUNT
git fetch deepHunt
git checkout -b localmaster deepHunt/master
git commit -am "ini commit"
git push deepHunt localmaster
```

Runing scripts:
<br />
```sh
cd deepHUNT/
ipython
execfile('sdf_utils/scripts/categorizeFile.py')
```
Once the sdf files are ready you can run maestro:
<br />
```sh
maestro17
```
in maestro: File -> Import Structures -> choose .sdf files <br />
Now you have all molecules in the project table. You can view project table Window -> Project Table <br />
Next step is to run the python scripts on all the molecules: Window -> Python Shell <br />
This will open an ipython shell <br />
<br />
```sh
execfile('maestro_utils/summaryScript.py')
```
If you accidently commit huges files, do this:
<br />
```sh
git rm --cached <hugefile>
git commit --amend -CHEAD
git push dhunt localmaster
```

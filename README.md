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


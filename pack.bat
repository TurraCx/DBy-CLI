pyinstaller -F -i=dby.ico app.py
copy dist\app.exe .\
rename app.exe DanishBytes.exe
rmdir dist /q /s
rmdir build /q /s
rmdir __pycache__ /q /s
del app.spec
# opcua_gui

## Per convertire l'interfaccia grafica UI in codice python:
```
 pyuic5 -x OPCUA.ui -o app.py
```

## Creazione del file EXE per windows:

### Librerie necessarie:
```
pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip
```

### comandi da eseguire
```
aprire cmd dalla cartella in cui vi è il file python
set PATH=%PATH%;C:\Windows\System32\downlevel;
pyinstaller.exe --onefile --windowed app.py
```



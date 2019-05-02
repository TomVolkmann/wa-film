# wa-film

NICHT PULLEN BEVOR NICHT ALLE LOKALEN FILECHANGES GE-STASHED WURDEN

# Umgebungsvorbereitung 

1. Visual Studio code
2. Python.org (3.7)
3. Terminal python ausprobieren 
4. Windows Umgebungsvariable (Path) setzen falls python nicht geht
5. Wa-Film clone and open
6. Python -m venv venv  (virtuelle Umgebung "venv" erstellen)
7. venv\Scripts\activate 
8. pip install -r requirements.txt (Pakete von Requirements installieren)
9. ~~set FLASK_APP-microblog.py  (Flask Umgebungsvariable setzen)~~
10. flask run (Server starten)
11. Install pylint (Syntax Highlighting)

## Info 
These two files will be ignored because they are different on each machine

app/__pycache__/__init__.cpython-37.pyc
app/__pycache__/routes.cpython-37.pyc 

Whenever anything is used in routes (import from Flask-Application (app))
It needs to be added in __init__.py too. 


#Flask Framework (Webserver)

#Angular angularJS
1. Install Node.js and Npm from https://nodejs.org/en/download/
2. Install Angular CLI npm install -g @angular/cli
# All-in-one - Windows
```
python -m venv .venv
.venv\Scripts\Activate
python -m pip install -r requirements.txt
cd webapp
python manage.py migrate
python manage.py runserver
```

# All-in-one - Linux
```
python -m venv .venv
chmod +x .venv/bin/activate
. .venv/bin/activatepython -m pip install -r requirements.txt
cd webapp
python manage.py migrate
python manage.py runserver
```

# One-by-one

### Set up a virtual environment:
```
python -m venv .venv
```

### Switch to a virtual environment in a terminal
Windows:
```
.venv\Scripts\Activate
```
Linux/WSL:
```
chmod +x .venv/bin/activate
. .venv/bin/activate
```

### Install all dependencies in an env
```
python -m pip install -r requirements.txt
```

### Run local server
```
cd webapp
python manage.py migrate
python manage.py runserver
```

### Credentials
`admin:admin`

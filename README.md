# All-in-one - Windows
```
git clone https://github.com/0Jan2137/projekt_aplikacja.git
python -m venv .venv
.venv\Scripts\Activate
python -m pip install -r requirements.txt
cd projekt_aplikacja\webapp
python manage.py migrate
python manage.py runserver
```

# All-in-one - Linux
```
git clone https://github.com/0Jan2137/projekt_aplikacja.git
python -m venv .venv
chmod +x .venv/bin/activate
. .venv/bin/activatepython -m pip install -r requirements.txt
cd projekt_aplikacja\webapp
python manage.py migrate
python manage.py runserver
```

# One-by-one
### Clone repo
```
git clone https://github.com/0Jan2137/projekt_aplikacja.git
```

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
cd projekt_aplikacja\webapp
python manage.py migrate
python manage.py runserver
```

### Credentials
`admin:admin`

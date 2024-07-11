![GitHub Logo](/gem/web/static/logo.svg)

Application to improve GBC meeting experience

# Installation
## Dependencies
1. Install https://wkhtmltopdf.org/
2. Install python requirements:
```
pip3 install -r requirements.txt
```

## Assets
Compile assets and seed a database
```
python3 ./tools/assets_compile.py
python3 ./install.py
```

# Development
Run development server
```
export FLASK_DEBUG=1
flask run
```

Run watchdog to compile assets automatically
```
pip3 install watchdog
python3 ./tools/assets_watchdog.py
```

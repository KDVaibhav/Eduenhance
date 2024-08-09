# Start Virtual Environment
  python -m venv venv 
  .\venv\Scripts\Activate

# Installing dependencies
  pip install -r requirements.txt

# Assets compilation
  python3 ./tools/assets_compile.py
  python3 ./install.py

# ENVIRONMENT VARIABLES
  set FLASK_DEBUG=1
  set FLASK_APP=app.py

# Start app
  flask run

# Automatic compilation
  pip3 install watchdog
  python3 ./tools/assets_watchdog.py


# Error during Flask Run

Error: While importing 'app', an ImportError was raised.


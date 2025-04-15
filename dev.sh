#!/bin/sh

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_ENV=development
flask run
trap "pip freeze > requirements.txt && deactivate"

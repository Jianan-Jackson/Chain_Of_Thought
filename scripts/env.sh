#!/bin/bash

# check if the venv directory exists
if [ ! -d "venv" ] 
then
    python3 -m venv venv
fi

source venv/bin/activate

# check if all requirements are installed
pip freeze > installed.txt
if ! cmp --silent installed.txt requirements.txt
then
    pip install -r requirements.txt
fi

rm installed.txt
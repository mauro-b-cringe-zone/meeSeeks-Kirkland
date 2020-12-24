#!/bin/bash

pwd

python3 -m venv pyenv
source pyvenv/bin/activate

pip3 install -r requirements.txt

python3 ./src/main.py --cmd run
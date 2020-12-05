@echo off

if(%1% == "i") pip install -r requirements.txt

python ./src/main.py --cmd run
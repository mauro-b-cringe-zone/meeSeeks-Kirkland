@echo off

python -m venv env
.\env\Scripts\activate

pip install -r requirements.txt

python ./src/main.py --cmd run
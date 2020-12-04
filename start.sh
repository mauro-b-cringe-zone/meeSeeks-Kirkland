#!/bin/bash

if [$1] == "i" 
then
    pwd
    pip3 install -r requirements.txt
fi

python3 ./src/main.py --cmd run
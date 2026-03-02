#!/bin/bash
cd "$(dirname "$0")"
pip3 install -r requirements.txt -q
python3 main.py

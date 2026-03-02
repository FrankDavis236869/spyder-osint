@echo off
chcp 65001 >nul
title Spyder OSINT GUI

cd /d "%~dp0"
pip install -r requirements.txt -q
python main.py
pause

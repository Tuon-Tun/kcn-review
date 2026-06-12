@echo off
rem Bấm đúp file này để mở giao diện web KCN Review
cd /d "%~dp0"
start "" http://127.0.0.1:8765
python webapp\app.py
pause

@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
cd /d "C:\Users\Admin\news_automation"
"C:\Users\Admin\AppData\Local\Python\pythoncore-3.14-64\python.exe" main.py run >> "C:\Users\Admin\news_automation\logs\automacao.log" 2>&1

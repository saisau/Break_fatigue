@echo off
:: 文字化け防止
chcp 65001

:: 仮想環境のパスを指定 (あなたの環境に合わせて書き換えてください)
:: 例: C:\Users\Seigo\Projects\fatigue-research-system
cd /d %~dp0

:: 仮想環境をアクティブ化してランナーを実行
call venv\Scripts\activate
python launcher.py

pause


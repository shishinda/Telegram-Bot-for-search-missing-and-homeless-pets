@echo off

call %~dp0C:\telegram_bot_pets\venv\Scripts\activate

cd %~dp0C:\telegram_bot_pets

set TOKEN=6062147358:AAEjI2QElKAyhOsB_mpHIrt3XK9CzC8Xil8

python C:\telegram_bot_pets\bot_telegram.py

pause
@echo off
echo Clearing Python cache...
del /s /q __pycache__ 2>nul
del /s /q *.pyc 2>nul

echo.
echo Starting Graive AI...
echo.
python graive.py

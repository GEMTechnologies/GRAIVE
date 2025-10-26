@echo off
cls
echo.
echo ========================================
echo    TESTING PROGRESS TRACKING
echo ========================================
echo.
echo This will test the new progress visibility features.
echo.
echo Try these commands when Graive AI starts:
echo.
echo 1. am [your name]
echo 2. write an essay about climate change in 1000 words
echo.
echo You should see:
echo  - Real-time API connection status
echo  - Word count as it's generated
echo  - File path when saved
echo  - Workspace contents automatically
echo.
echo ========================================
echo.
pause
python graive.py

@echo off
REM === 1) Activate the 'lynx' conda env ===
call "%USERPROFILE%\miniconda3\Scripts\activate.bat" lynx

REM === 2) Go to your project folder ===
cd /d "C:\Users\Zoki\Desktop\Lynx Python"

REM === 3) Run the Streamlit app ===
streamlit run lynx_app.py

REM Keep window open if something goes wrong
pause

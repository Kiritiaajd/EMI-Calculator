@echo off
echo.
echo ===============================
echo EMI Calculator Setup Script
echo ===============================
echo.

:: Step 1: Create a new Conda environment
echo Creating conda environment 'emi_calculator_env'...
conda create -y -n emi_calculator_env python=3.9

:: Step 2: Activate the environment
echo Activating environment...
call conda activate emi_calculator_env

:: Step 3: Install required packages
echo Installing dependencies...
pip install -r requirements.txt

:: Step 4: Launch the Streamlit App
echo Launching the Streamlit EMI Calculator app...
streamlit run app.py

pause

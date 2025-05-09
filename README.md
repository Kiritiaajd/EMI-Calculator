# EMI Calculator (Streamlit App)

This is an interactive EMI calculation tool that computes monthly payments and generates a full amortization schedule with interest rate revisions.

## Features

- Calculate EMI using principal, rate, and tenure.
- Handle multiple interest rate changes.
- Download amortization table as CSV.

## Requirements

- Python 3.9+
- Conda (Anaconda/Miniconda)

## Setup Instructions (Windows)

1. Clone or download this repo.
2. Double-click the `setup_env.bat` file to automatically:
   - Create a conda environment.
   - Install dependencies.
   - Launch the app in your browser.

## Manual Setup (if preferred)

```bash
conda create -n emi_calculator_env python=3.9
conda activate emi_calculator_env
pip install -r requirements.txt
streamlit run app.py

# backend/scenarios_03.py

import math
import pandas as pd


def calculate_adjusted_emi_and_tenure(principal, old_rate, new_rate, tenure_years, max_emi_increase_per_percent):
    # Step 1: Calculate original EMI based on old interest rate
    tenure_months = tenure_years * 12
    emi_old = (principal * old_rate / 100 / 12) * (1 + old_rate / 100) ** tenure_months / ((1 + old_rate / 100) ** tenure_months - 1)

    # Step 2: Calculate new EMI based on new interest rate
    emi_new = (principal * new_rate / 100 / 12) * (1 + new_rate / 100) ** tenure_months / ((1 + new_rate / 100) ** tenure_months - 1)

    # Step 3: Calculate the EMI difference
    delta_emi = emi_new - emi_old

    # Step 4: Determine EMI burden ratio (for reference)
    emi_burden_ratio = delta_emi / emi_old

    # Step 5: Calculate the new tenure if EMI is adjusted, based on max EMI increase policy
    tenure_burden_ratio = 0  # Initialize tenure_burden_ratio to avoid UnboundLocalError
    if emi_burden_ratio > 0:
        tenure_burden_ratio = emi_burden_ratio * (1 / max_emi_increase_per_percent)  # Calculate the tenure adjustment
        final_tenure = int(tenure_months * (1 + tenure_burden_ratio))  # Adjust tenure based on the burden
    else:
        final_tenure = tenure_months  # If no increase, tenure stays the same

    # Step 6: Calculate final EMI and tenure
    final_emi = emi_new
    return {
        "emi_old": round(emi_old, 2),
        "emi_new_full": round(emi_new, 2),
        "delta_emi": round(delta_emi, 2),
        "emi_burden_ratio": round(emi_burden_ratio, 4),
        "tenure_burden_ratio": round(tenure_burden_ratio, 4),  # Always include tenure_burden_ratio
        "final_emi": round(final_emi, 2),
        "final_tenure": final_tenure
    }

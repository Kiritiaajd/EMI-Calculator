import math
import pandas as pd

def calculate_emi(principal, annual_rate, tenure_years):
    tenure_months = tenure_years * 12
    monthly_rate = annual_rate / 12 / 100
    emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
    return round(emi, 2)

def generate_full_schedule(principal, emi, original_rate, tenure_months, rate_changes):
    schedule = []
    balance = principal
    rate_changes = sorted(rate_changes, key=lambda x: x[0])
    current_rate = original_rate
    current_change_index = 0

    for month in range(1, tenure_months + 1):
        if current_change_index < len(rate_changes) and month == rate_changes[current_change_index][0]:
            current_rate = rate_changes[current_change_index][1]
            current_change_index += 1

        monthly_rate = current_rate / 12 / 100
        interest = balance * monthly_rate
        principal_paid = emi - interest
        balance -= principal_paid
        balance = max(balance, 0)

        schedule.append({
            "Month": month,
            "EMI (₹)": round(emi, 2),
            "Principal Paid (₹)": round(principal_paid, 2),
            "Interest Paid (₹)": round(interest, 2),
            "Remaining Balance (₹)": round(balance, 2),
            "Interest Rate (Annual) [%]": round(current_rate, 2),
        })

        if balance <= 0:
            break

    return pd.DataFrame(schedule)

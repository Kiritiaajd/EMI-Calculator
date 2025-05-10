import math
import pandas as pd

def calculate_emi(principal, annual_rate, tenure_years):
    tenure_months = tenure_years * 12
    monthly_rate = annual_rate / 12 / 100
    emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
    return round(emi, 2)

def calculate_new_tenure(principal, emi, annual_rate):
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate == 0:
        return principal / emi

    if emi <= principal * monthly_rate:
        raise ValueError("EMI is too low relative to the principal and interest rate for the given calculation.")

    tenure_months = math.log(emi / (emi - principal * monthly_rate)) / math.log(1 + monthly_rate)
    return math.ceil(tenure_months)

def generate_full_schedule(principal, emi, original_rate, original_tenure_months, rate_changes):
    schedule = []
    balance = principal
    rate_changes = sorted(rate_changes, key=lambda x: x[0])
    current_rate = original_rate
    current_change_index = 0
    current_month = 1

    # Initial tenure based on EMI
    monthly_rate = current_rate / 12 / 100
    remaining_months = calculate_new_tenure(balance, emi, current_rate)

    change_summaries = []

    while balance > 0:
        # Apply rate change if needed
        if current_change_index < len(rate_changes) and current_month == rate_changes[current_change_index][0]:
            previous_remaining = remaining_months
            current_rate = rate_changes[current_change_index][1]
            monthly_rate = current_rate / 12 / 100

            try:
                remaining_months = calculate_new_tenure(balance, emi, current_rate)
            except:
                remaining_months = 0

            tenure_diff = remaining_months - previous_remaining

            change_summaries.append({
                "change_month": current_month,
                "new_rate": round(current_rate, 2),
                "previous_remaining": previous_remaining,
                "new_remaining": remaining_months,
                "tenure_diff": tenure_diff
            })

            current_change_index += 1

        # EMI breakdown
        interest = balance * monthly_rate
        principal_paid = emi - interest

        if principal_paid <= 0:
            raise ValueError("EMI is too low for the current interest rate. Loan will never be repaid.")

        balance -= principal_paid
        balance = max(balance, 0)

        try:
            remaining_months = calculate_new_tenure(balance, emi, current_rate) if balance > 0 else 0
        except:
            remaining_months = 0

        schedule.append({
            "Month": current_month,
            "EMI (₹)": round(emi, 2),
            "Principal Paid (₹)": round(principal_paid, 2),
            "Interest Paid (₹)": round(interest, 2),
            "Remaining Balance (₹)": round(balance, 2),
            "Interest Rate (Annual) [%]": round(current_rate, 2),
            "Remaining Tenure (Months)": remaining_months
        })

        current_month += 1

    return pd.DataFrame(schedule), change_summaries

import math
import pandas as pd

def calculate_emi(principal, annual_rate, tenure_years):
    tenure_months = tenure_years * 12
    monthly_rate = annual_rate / 12 / 100
    emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
    return round(emi, 2)

def calculate_emi_with_tenure(principal, annual_rate, remaining_months):
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate == 0:
        return round(principal / remaining_months, 2)

    emi = principal * monthly_rate * ((1 + monthly_rate) ** remaining_months) / (((1 + monthly_rate) ** remaining_months) - 1)
    return round(emi, 2)

def generate_schedule_fixed_tenure(principal, original_rate, original_tenure_years, rate_changes):
    schedule = []
    rate_changes = sorted(rate_changes, key=lambda x: x[0])
    total_months = original_tenure_years * 12
    current_month = 1
    balance = principal
    current_rate = original_rate
    emi = calculate_emi(principal, original_rate, original_tenure_years)

    current_change_index = 0
    rate_summary = []

    while current_month <= total_months and balance > 0:
        # Apply rate change if applicable
        if current_change_index < len(rate_changes) and current_month == rate_changes[current_change_index][0]:
            current_rate = rate_changes[current_change_index][1]
            remaining_months = total_months - current_month + 1
            new_emi = calculate_emi_with_tenure(balance, current_rate, remaining_months)

            rate_summary.append({
                "Change Month": current_month,
                "New Rate": current_rate,
                "Previous EMI": round(emi, 2),
                "New EMI": round(new_emi, 2),
                "Change (₹)": round(new_emi - emi, 2),
                "Remaining Tenure (Months)": remaining_months
            })

            emi = new_emi
            current_change_index += 1

        monthly_rate = current_rate / 12 / 100
        interest = balance * monthly_rate
        principal_paid = emi - interest

        if principal_paid < 0:
            raise ValueError("EMI too low for the current interest rate. Loan will never be repaid.")

        balance -= principal_paid
        balance = max(balance, 0)

        schedule.append({
            "Month": current_month,
            "EMI (₹)": round(emi, 2),
            "Principal Paid (₹)": round(principal_paid, 2),
            "Interest Paid (₹)": round(interest, 2),
            "Remaining Balance (₹)": round(balance, 2),
            "Interest Rate (Annual) [%]": round(current_rate, 2),
        })

        current_month += 1

    df_schedule = pd.DataFrame(schedule)
    df_summary = pd.DataFrame(rate_summary)
    return df_schedule, df_summary

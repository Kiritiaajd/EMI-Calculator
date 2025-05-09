import streamlit as st
import pandas as pd
from backend.scenarios_01 import calculate_emi, generate_full_schedule

def main():
    st.title("EMI Calculation and Schedule Generator")
    
    # Input for Loan Details
    st.header("Loan Details")
    col1, col2 = st.columns(2)
    with col1:
        principal = st.number_input("Loan Amount (₹)", min_value=10000, step=1000, value=800000, key="principal")
    with col2:
        annual_rate = st.number_input("Annual Interest Rate (%)", min_value=0.1, value=11.20, key="rate")
    
    tenure_years = st.number_input("Loan Tenure (Years)", min_value=1, value=5, key="tenure")
    
    # Automatically calculate EMI whenever input changes
    emi = calculate_emi(principal, annual_rate, tenure_years)
    st.session_state.emi = emi
    st.write(f"Calculated EMI: ₹{emi}")
    
    # Input for Interest Rate Changes
    st.header("Interest Rate Changes")
    rate_changes = []
    rate_change_input_count = st.number_input("Number of Rate Changes", min_value=0, max_value=10, value=0, key="rate_change_count")
    
    for i in range(int(rate_change_input_count)):
        col1, col2 = st.columns(2)
        with col1:
            change_month = st.number_input(f"Change Month for Rate {i+1} (Months)", min_value=1, value=12, key=f"change_month_{i}")
        with col2:
            change_rate = st.number_input(f"New Interest Rate for Change {i+1} (%)", min_value=0.1, value=12.5, key=f"change_rate_{i}")
        
        rate_changes.append((change_month, change_rate))

    
    if rate_change_input_count > 0:
        if st.button("Generate EMI Schedule"):
            tenure_months = tenure_years * 12
            schedule_df = generate_full_schedule(principal, emi, annual_rate, tenure_months, rate_changes)
            st.subheader("EMI Schedule")
            st.write(schedule_df)

            # Provide option to download the schedule as CSV
            csv = schedule_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download EMI Schedule (CSV)",
                data=csv,
                file_name="emi_schedule.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()

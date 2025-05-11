import streamlit as st
import pandas as pd
from backend.scenarios_01 import calculate_emi as calculate_emi_s1, generate_full_schedule
from backend.scenarios_02 import calculate_emi as calculate_emi_s2, generate_schedule_fixed_tenure
from backend.scenarios_03 import calculate_adjusted_emi_and_tenure  # Import the new function

def main():
    st.title("EMI Calculator & Dynamic Schedule Generator")

    # Choose Scenario
    scenario = st.radio(
        "Select EMI Scenario",
        (
            "Scenario 1: Constant EMI, Changing Tenure",
            "Scenario 2: Changing EMI, Constant Tenure",
            "Scenario 3: Adjust Both EMI & Tenure"  # Added Scenario 3 option
        )
    )

    # Loan Details Input
    st.header("Loan Details")
    col1, col2 = st.columns(2)
    with col1:
        principal = st.number_input("Loan Amount (₹)", min_value=10000, step=1000, value=800000)
    with col2:
        annual_rate = st.number_input("Initial Annual Interest Rate (%)", min_value=0.1, value=11.20)

    tenure_years = st.number_input("Loan Tenure (Years)", min_value=1, value=5)

    # Scenario 1: Constant EMI, Changing Tenure
    if scenario == "Scenario 1: Constant EMI, Changing Tenure":
        emi = calculate_emi_s1(principal, annual_rate, tenure_years)
        st.write(f"Calculated EMI (Fixed): ₹{emi}")

    # Scenario 2: Changing EMI, Constant Tenure
    elif scenario == "Scenario 2: Changing EMI, Constant Tenure":
        emi = calculate_emi_s2(principal, annual_rate, tenure_years)
        st.write(f"Initial EMI (Variable): ₹{emi}")

    # Scenario 3: Adjust Both EMI & Tenure (New Scenario)
    elif scenario == "Scenario 3: Adjust Both EMI & Tenure":
        max_emi_increase_per_percent = 1000  # Policy-defined maximum increase per 1% rate change
        result = calculate_adjusted_emi_and_tenure(principal, annual_rate, annual_rate, tenure_years, max_emi_increase_per_percent)

        # Ensure the result has the correct keys
        if 'emi_old' in result and 'final_emi' in result and 'final_tenure' in result:
            st.write(f"Initial EMI: ₹{result['emi_old']}")
            st.write(f"Adjusted EMI: ₹{result['final_emi']}")
            st.write(f"Adjusted Tenure: {result['final_tenure']} months")
        else:
            st.error("Error: Missing key values in the result.")
            st.write(result)  # Optionally display the result dictionary to debug

    # Rate Changes
    st.header("Interest Rate Changes")
    rate_changes = []
    rate_change_input_count = st.number_input("Number of Rate Changes", min_value=0, max_value=10, value=0)

    for i in range(int(rate_change_input_count)):
        col1, col2 = st.columns(2)
        with col1:
            change_month = st.number_input(f"Change Month #{i+1}", min_value=1, value=12, key=f"change_month_{i}")
        with col2:
            change_rate = st.number_input(f"New Rate at Month #{i+1} (%)", min_value=0.1, value=12.5, key=f"change_rate_{i}")
        rate_changes.append((change_month, change_rate))

    # Generate Schedule
    if st.button("Generate EMI Schedule"):
        tenure_months = tenure_years * 12

        if scenario == "Scenario 1: Constant EMI, Changing Tenure":
            schedule_df, change_summaries = generate_full_schedule(
                principal, emi, annual_rate, tenure_months, rate_changes
            )

            # Summary Display
            if change_summaries:
                st.subheader("Interest Rate Change Summary")
                for change in change_summaries:
                    with st.container():
                        st.markdown(f"""
                         **Interest rate changed at Month {change['change_month']}**  
                        - New Interest Rate: **{change['new_rate']}%**  
                        - Previous Remaining Tenure: **{change['previous_remaining']} months**  
                        - New Remaining Tenure: **{change['new_remaining']} months**  
                        {"→ Tenure increased by" if change['tenure_diff'] > 0 else "→ Tenure reduced by"} **{abs(change['tenure_diff'])} months**
                        """)

        else:  # Scenario 2
            schedule_df, summary_df = generate_schedule_fixed_tenure(
                principal, original_rate=annual_rate, original_tenure_years=tenure_years, rate_changes=rate_changes
            )

            if not summary_df.empty:
                st.subheader("EMI Change Summary")
                for _, row in summary_df.iterrows():
                    st.markdown(f"""
                     **Interest rate changed at Month {int(row['Change Month'])}**  
                    - New Interest Rate: **{row['New Rate']}%**  
                    - Previous EMI: **₹{row['Previous EMI']}**  
                    - New EMI: **₹{row['New EMI']}**  
                    {"→ EMI increased by" if row['Change (₹)'] > 0 else "→ EMI reduced by"} **₹{abs(row['Change (₹)'])}**  
                    - Remaining Tenure: **{int(row['Remaining Tenure (Months)'])} months**
                    """)

        # Show EMI Table
        st.subheader("EMI Repayment Schedule")
        st.dataframe(schedule_df, use_container_width=True)

        # Download
        csv = schedule_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Schedule as CSV", data=csv, file_name="emi_schedule.csv", mime="text/csv")

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import joblib
import subprocess


# Dummy Aadhar numbers for demonstration purposes
verified_aadhar_numbers = {'JohnDoe': '123456789012', 'JaneDoe': '987654321098', 'Aarone George': '999507201622'}
verification_result = st.empty()


def aadhar_verification():
    st.title("Aadhar Verification")
    username = st.text_input('Enter your username')
    aadhar_number = st.text_input('Enter your Aadhar number')
    if st.button('Verify Aadhar'):
        if username in verified_aadhar_numbers and aadhar_number == verified_aadhar_numbers[username]:
            st.success("Aadhar verification successful! Proceed to loan prediction.")
            verification_result.markdown('[Proceed to Loan Prediction](#loan_prediction)')
            
            cmd_command = 'streamlit run ./pred.py'

            subprocess.run(cmd_command, shell=True)

        else:
            st.error("Aadhar verification failed. Please check your username and Aadhar number.")
            st.stop()

aadhar_verification()
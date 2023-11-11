import streamlit as st
import pandas as pd
import joblib
import subprocess

model = joblib.load('loan_status_predict')

st.title("Loan Prediction")

Loan_ID = st.text_input('Enter Loan ID')
Gender = st.selectbox('Gender', ['Male', 'Female'])
Married = st.selectbox('Married', ['Yes', 'No'])
Dependents = st.number_input('Dependents')
Education = st.selectbox('Education', ['Graduate', 'Not Graduate'])
Self_Employed = st.selectbox('Self Employed', ['Yes', 'No'])
ApplicantIncome = st.number_input('Applicant Income per Annum (In rupees)') /83
CoapplicantIncome = st.number_input('Co-Applicant Income per Annum (In rupees)')/83
LoanAmount = st.number_input('Loan Amount (In lakhs)')
Loan_Amount_Term = st.number_input('Loan Term (In Months)')
Credit_History = (st.number_input('Credit Score') + 100)/1000 
Property_Area = st.selectbox('Property Area', ['Rural', 'Semiurban', 'Urban'])

# Encode categorical variables
Gender_mapping = {'Male': 1, 'Female': 0}
Married_mapping = {'Yes': 1, 'No': 0}
Education_mapping = {'Graduate': 1, 'Not Graduate': 0}
Self_Employed_mapping = {'Yes': 1, 'No': 0}
Property_Area_mapping = {'Rural': 0, 'Semiurban': 2, 'Urban': 1}
Loan_Status_mapping = {'Y': 1, 'N': 0}

# Apply mapping
Gender = Gender_mapping.get(Gender, -1)
Married = Married_mapping.get(Married, -1)
Education = Education_mapping.get(Education, -1)
Self_Employed = Self_Employed_mapping.get(Self_Employed, -1)
Property_Area = Property_Area_mapping.get(Property_Area, -1)

# Create a DataFrame with the input data
data = pd.DataFrame({
    'Gender': [Gender],
    'Married': [Married],
    'Dependents': [Dependents],
    'Education': [Education],
    'Self_Employed': [Self_Employed],
    'ApplicantIncome': [ApplicantIncome],
    'CoapplicantIncome': [CoapplicantIncome],
    'LoanAmount': [LoanAmount],
    'Loan_Amount_Term': [Loan_Amount_Term],
    'Credit_History': [Credit_History],
    'Property_Area': [Property_Area]
})

data.to_csv('data.csv', index=False)


if st.button('Check'):

    prediction = model.predict(data)[0]

    if prediction == 1:
        display = "Loan is approved"
        st.title(display)
        cmd_command = 'streamlit run ./cus_profile.py'
        subprocess.run(cmd_command, shell=True)
    else:
        display = "Loan is not approved"
        st.title(display)
        cmd_command = 'streamlit run ./cus_profile.py'
        subprocess.run(cmd_command, shell=True)

    




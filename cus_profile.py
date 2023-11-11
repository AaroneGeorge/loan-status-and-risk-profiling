import streamlit as st
import pandas as pd

df = pd.read_csv('data.csv')

row_index = 0
Gender = df.at[row_index, 'Gender']
Married = df.at[row_index, 'Married']
Dependents = df.at[row_index, 'Dependents']
Education = df.at[row_index, 'Education']
Self_Employed = df.at[row_index, 'Self_Employed']
ApplicantIncome = df.at[row_index, 'ApplicantIncome']
CoapplicantIncome = df.at[row_index, 'CoapplicantIncome']
LoanAmount = df.at[row_index, 'LoanAmount']
Loan_Amount_Term = df.at[row_index, 'Loan_Amount_Term']
Credit_History = df.at[row_index, 'Credit_History']
Property_Area = df.at[row_index, 'Property_Area']


def roi(lat=1):
    if lat < 3:
        ir = 0.4
    elif lat < 60:
        ir = 0.55
    else:
        ir = 0.6

    roi_value = ir * 100 / (lat/12)

    return roi_value


def pti(tla, inc=1):
    pti_value = tla *100/ inc

    return pti_value


def raroc(tla=1, lat=1):
    if lat < 3:
        ir = 0.4
    elif lat < 60:
        ir = 0.55
    else:
        ir = 6

    exp_ret = tla + (tla * ir * lat)

    raroc_value = exp_ret / (exp_ret + 100000)

    return raroc_value


def ltv(tla):

    prop_val = tla + 0.5 * tla
    ltv_value = tla * 100 / prop_val

    return ltv_value


def dti(tla=1, lat=1, sal=1):
    dti_value = tla * 12 * 100 / (lat * sal)

    return dti_value


def riskScore(roi, pti, raroc, ltv, dti):
    risk_score = -0.1 * roi + 0.25 * pti + -0.2 * raroc + 0.25 * ltv + 0.15 * dti
    return risk_score


st.title("Customer Risk Profile")

roi_value = roi(Loan_Amount_Term)
st.markdown("## ROI (Return On Investment): "+ str(roi_value))

pti_value = pti(LoanAmount, ApplicantIncome + CoapplicantIncome)
st.markdown("## PTI (Payment To Income): "+ str(pti_value))

raroc_value = raroc(LoanAmount, Loan_Amount_Term)
st.markdown("## RAROC (Risk Adjusted Return On Capital): "+ str(raroc_value))

ltv_value = ltv(LoanAmount)
st.markdown("## LTV (Loan To Value) : "+ str(ltv_value))

dti_value = dti(Loan_Amount_Term, LoanAmount, ApplicantIncome + CoapplicantIncome)
st.markdown("## DTI (Debt To Income) : "+ str(dti_value))

customer_risk_score = riskScore(roi_value, pti_value, raroc_value, ltv_value, dti_value)
st.title("Customer Risk Score: "+ str(customer_risk_score))

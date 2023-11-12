import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

# Display ROI with description
st.markdown("## ROI (Return On Investment): ")
st.text("Return On Investment (ROI) is calculated based on the loan term.")
st.text("ROI = (Interest Rate * 100) / (Loan Term (in years) / 12)")
roi_value = roi(Loan_Amount_Term)
st.write(f"ROI Value: {roi_value}")

# Display PTI with description
st.markdown("## PTI (Payment To Income): ")
st.text("Payment To Income (PTI) ratio represents the percentage of income used for loan payments.")
st.text("PTI = (Total Loan Amount * 100) / Total Income")
pti_value = pti(LoanAmount, ApplicantIncome + CoapplicantIncome)
st.write(f"PTI Value: {pti_value}")

# Display RAROC with description
st.markdown("## RAROC (Risk Adjusted Return On Capital): ")
st.text("Risk Adjusted Return On Capital (RAROC) considers risk when calculating return on investment.")
st.text("RAROC = Expected Return / (Expected Return + Risk Capital)")
raroc_value = raroc(LoanAmount, Loan_Amount_Term)
st.write(f"RAROC Value: {raroc_value}")

# Display LTV with description
st.markdown("## LTV (Loan To Value): ")
st.text("Loan To Value (LTV) ratio represents the percentage of the loan amount to the appraised value of the property.")
st.text("LTV = (Total Loan Amount * 100) / Appraised Value of Property")
ltv_value = ltv(LoanAmount)
st.write(f"LTV Value: {ltv_value}")

# Display DTI with description
st.markdown("## DTI (Debt To Income): ")
st.text("Debt To Income (DTI) ratio represents the percentage of income used for debt payments.")
st.text("DTI = (Total Loan Amount * 12 * 100) / (Loan Term (in years) * Total Income)")
dti_value = dti(Loan_Amount_Term, LoanAmount, ApplicantIncome + CoapplicantIncome)
st.write(f"DTI Value: {dti_value}")

# Calculate and Display Customer Risk Score
customer_risk_score = riskScore(roi_value, pti_value, raroc_value, ltv_value, dti_value)
st.title("Customer Risk Score:")
st.write(f"Customer Risk Score: {customer_risk_score}")


user_data = pd.read_csv('data.csv')
loan_dataset = pd.read_csv('loan_dataset.csv')

def dataclean(data):
    data = data.drop('Loan_ID',axis=1)
    columns = ['Gender','Dependents','LoanAmount','Loan_Amount_Term']
    data = data.dropna(subset=columns)
    data['Self_Employed'] =data['Self_Employed'].fillna(data['Self_Employed'].mode()[0])
    data['Credit_History'] =data['Credit_History'].fillna(data['Credit_History'].mode()[0])
    data['Dependents'] =data['Dependents'].replace(to_replace="3+",value='4')
    data['Dependents'].unique()
    data['Loan_Status'].unique()
    data['Gender'] = data['Gender'].map({'Male':1,'Female':0}).astype('int')
    data['Married'] = data['Married'].map({'Yes':1,'No':0}).astype('int')
    data['Education'] = data['Education'].map({'Graduate':1,'Not Graduate':0}).astype('int')
    data['Self_Employed'] = data['Self_Employed'].map({'Yes':1,'No':0}).astype('int')
    data['Property_Area'] = data['Property_Area'].map({'Rural':0,'Semiurban':2,'Urban':1}).astype('int')
    data['Loan_Status'] = data['Loan_Status'].map({'Y':1,'N':0}).astype('int')

    return data


loan_dataset = dataclean(loan_dataset)

plt.figure(figsize=(16, 14)) 

# Set the size of the entire image
plt.figure(figsize=(21 , 19))


# Create a heatmap of correlations between datasets
correlation_matrix = pd.concat([user_data, loan_dataset], axis=1).corr()

# Create the heatmap with consistent text size
heatmap = sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", annot_kws={"size": 13}, cbar_kws={'label': 'Correlation'})

# Increase the font size for x-axis and y-axis labels
plt.xticks(rotation=45, ha='right', fontsize=15)
plt.yticks(fontsize=15)

# Adjust the outer axis to scale the heatmap
plt.subplots_adjust(left=0.1 , right=0.9, top=0.9, bottom=0.1)

# Display the heatmap
st.title("Heatmap Comparison of User Data and Loan Dataset")
st.pyplot(heatmap.get_figure())


# scatterplot : income v/s loan Amount
plt.figure(figsize=(10, 8))

# Create a scatter plot of income versus loan amount
scatter_plot = sns.scatterplot(x='ApplicantIncome', y='LoanAmount', data=loan_dataset, palette='Set1')
scatter_plot = sns.scatterplot(x='ApplicantIncome', y='LoanAmount', data=user_data, marker = 'X' , color = 'red')

# Customize the plot
plt.title('Income vs Loan Amount Scatter Plot')
plt.xlabel('Applicant Income')
plt.ylabel('Loan Amount')

# Display the scatter plot
st.pyplot(scatter_plot.get_figure())
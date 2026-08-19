## Six key steps in building a web app:
# 1. Import required libraries
# 2. Load your trained machine learning model
# 3. Write a function that will make the prediction
# 4. Build your Streamlit interface
# 5. Set up prediction button
# 6. Run the web app



### 1.Importing the required libraries
import pickle  # Helps load the train model
import numpy as np  # Convert user data to numpy array
import streamlit as st    # Major librray:it helps us build the web app



### 2. Load your trained machine learning model
load_model = pickle.load(open('model.sav', 'rb'))   # rb = read binary

### 3.Write a function that will make the prediction

def loan_prediction(input_data):
    input_array = np.array(input_data).reshape(1, -1) # ### converting the imput data to a numpy array
    prediction=load_model.predict(input_array)    # Make prediction using loaded model

    ## Writing a conditional statement for our prediction
    if prediction[0]==0:
        return('Sorry,You are not eligible for loan')
    else:
        return('Congratulations,You are eligible for loan')


# cd.onedrive
# Feature order used by the model (12 features):
# Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome,
# CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History,
# Rural, Semiurban, Urban
 
 
### 4. Build your Streamlit interface

def main():
    ## Loan web app heading
    st.title('Loan Prediction App')

    ## using 3 columns for the features
    col1,col2,col3=st.columns(3)


    # -----------------------------column one:Gender,Married,Dependents,Education
    with col1:
        Gender=st.selectbox('Gender',options=['Female','Male'])        # Select botton
        Married=st.selectbox('Married',options=['Yes','No'])
        Dependents=st.selectbox('Dependents',options=['0','1','2','3+'])
        Education=st.selectbox('Education',options=['Graduate','Not Graduate'])



    # -----------------------------column two:Self_Employed,ApplicantIncome,CoapplicantIncome,LoanAmount
    with col2:
        Self_Employed=st.selectbox('Self_Employed',options=['Yes','No'])        # Select botton
        ApplicantIncome=st.number_input('ApplicantIncome',min_value=0,value=0)   # Input values
        CoapplicantIncome=st.number_input('CoapplicantIncome',min_value=0,value=0)
        LoanAmount=st.number_input('LoanAmount',min_value=0,value=0)


    # -----------------------------column Three:Loan_Amount_Term,Credit_History,Property_Area(Rural,semi urban and rural)
    with col3:
        Loan_Amount_Term=st.number_input('Loan_Amount_Term',min_value=1,max_value=360,step=1) # Select because of the data type
        #Loan_Amount_Term=st.number_input('Loan_Amount_Term',min_values=1,max_value=360)  if its integer
        Credit_History=st.selectbox('Credit_History',options=['1 (Good)','0 (Bad)'])
        Property_Area=st.selectbox('Property_Area',options=['Urban','Semiurban','Rural'])




    #### set up the prediction button ---- Step 5
    if st.button('Bank Loan Application'):
        try:
            gender_val = 1 if Gender == 'Male' else 0
            married_val = 1 if Married == 'Yes' else 0
            dependents_val = 3 if Dependents == '3+' else int(Dependents)
            education_val = 1 if Education == 'Graduate' else 0  
            self_employed_val = 1 if Self_Employed == 'Yes' else 0
            credit_history_val = 1 if Credit_History.startswith('1') else 0 
            
            # Fixed completed Property Area encoding (Rural / Semiurban / Urban)
            rural_val = 1 if Property_Area == 'Rural' else 0
            semiurban_val = 1 if Property_Area == 'Semiurban' else 0
            urban_val = 1 if Property_Area == 'Urban' else 0
            
            # Next steps: build feature vector and pass to model.predict(...)
            
            input_data = [gender_val,
                          married_val,
                          dependents_val,
                          education_val,
                          self_employed_val,
                          ApplicantIncome,
                          CoapplicantIncome,
                          LoanAmount,
                          Loan_Amount_Term,
                          credit_history_val,
                          rural_val,
                          semiurban_val,
                          urban_val]

            # Call prediction function from Step 3
            Result = loan_prediction(input_data)

            # Display prediction result
            if 'Congratulations' in Result:
                st.success(Result)
            else:
                st.error(Result)

        except ValueError as ve:
            st.error(f'ValueError (Check feature shape): {ve}')


# Step 6: Run the web app
if __name__ == '__main__':
    main()
import streamlit as st # lets you build the web UI (form, buttons, sliders).
import requests

st.set_page_config(layout="wide") # sets the layout of the page to wide, so that it takes the full width of the browser window.
# Adds a page title at the top of the Streamlit app.
st.title("Churn Prediction API")

# FastAPI endpoint URL
API_URL = "https://customer-churn-predictor-b4et.onrender.com/api/predict"


# Building the input form
with st.form("churn_form"):
    credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=650) # value 650 is default value
    geography = st.selectbox("Geography", ["France", "Spain", "Germany"]) # dropdown
    gender = st.selectbox('Gender', ["Male", "Female"]) # dropdown
    age = st.slider("Age", min_value=18, max_value=80, value=30) # slider. default value is 30
    tenure = st.slider("Tenure (Years)", min_value=0, max_value=10, value=5) # slider. default value is 5
    balance = st.number_input("Balance", min_value=0.0, max_value=1000000.0, value=125000.0) # default value is 10000
    num_of_products = st.slider("Number of Products", 1, 4, 2)  # slider. default value is 2. automatically takes the min, max and value
    has_credit_card = st.checkbox("Has Credit Card") # checkbox
    is_active_member = st.checkbox("Is Active Member") # checkbox
    estimated_salary = st.number_input("Estimated Salary", min_value=0.0, value=50000.0) # default value is 50000
    
    submitted = st.form_submit_button("Predict Churn")
    
# After clicking the Predict button:
if submitted:
    # Prepare the input data as a dictionary
    input_data = {
        "CreditScore": credit_score,
        "geography": geography,
        "gender": gender,
        "Age": age,
        "tenure": tenure,
        "balance": balance,
        "NumOfProducts": num_of_products,
        "HasCrCard": has_credit_card,
        "IsActiveMember": is_active_member,
        "EstimatedSalary": estimated_salary
    }
    
    try:
        response = requests.post(API_URL, json = input_data, timeout = 5)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        result = response.json()  # Parse the JSON response
        
        st.success(f'Churn Probability: {result["churn_probability"]}, Will Churn: {result["will_churn"]}')
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")   
        

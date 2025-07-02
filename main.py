# loading necessary libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib, json, pandas as pd
from pathlib import Path

# loading artifacts, meaning at start-up we read the model, scaler, feature list, and threshold from disk once, so predictions are fast.
BASE_DIR = Path(__file__).resolve().parent
PIPELINE_DIR = BASE_DIR / "saved_pipeline"

model = joblib.load(PIPELINE_DIR / "rf_model.pkl")
scaler = joblib.load(PIPELINE_DIR / "rf_scaler.pkl")

with open(PIPELINE_DIR / "rf_features.json") as f:
    Features = json.load(f)
    
with open(PIPELINE_DIR / "rf_threshold.json") as f:
    Threshold = json.load(f)

# defining the request and response scripts/shapes
class churnRequestBody(BaseModel):
    credit_score: int = Field(..., alias = "CreditScore", description="Credit score of the customer")
    geography: str
    gender: str
    age: int = Field(..., ge=18, le=80, alias = "Age", description="Age of the customer")
    tenure: int = Field(ge=0, le=10)
    balance: float = Field(ge = 0)
    num_of_products: int = Field(ge=1, le=4, alias = "NumOfProducts", description="Number of products the customer has")
    has_credit_card: bool = Field(alias = "HasCrCard", description="Does the customer have a credit card?")
    is_active_member: bool = Field(alias = "IsActiveMember", description="Is the customer an active member?")
    estimated_salary: float = Field(ge=0, alias = "EstimatedSalary", description="Estimated salary of the customer")
    
class churnResponseBody(BaseModel):
    churn_probability: float
    will_churn: bool
    
# creating fastapi app
app = FastAPI(title="Churn Prediction API")

@app.get("/")
def root_route():
    return {"msg":"Churn Prediction API is live 🎊"}

@app.post("/predict", response_model = churnResponseBody)
def predict(body: churnRequestBody):
    print(body.dict(by_alias=True))
    try:
        #1. convert the input data into dataframe and turn the json into Python dictionary with exact keys like hasCreditCard.
        df = pd.DataFrame([body.dict(by_alias=True)])
        df = pd.get_dummies(df)  # Or use your original encoder
        df = df.reindex(columns=Features, fill_value=0)
        
        #2. scaling it like we did while training
        x_scaled = scaler.transform(df)
        
        #3.predict churn probability
        prob = float(model.predict_proba(x_scaled)[0][1])
        will_churn = prob > Threshold
        
        return churnResponseBody(churn_probability=round(prob, 3), will_churn=will_churn)              
                      
    except Exception as e:
        raise HTTPException(status_code = 500, detail=f'Inference error: {e}')

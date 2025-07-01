# customer-churn-predictor

This project demonstrates a full machine learning pipeline for predicting loan eligibility, deployed using both a **FastAPI backend** and a **Streamlit frontend**.

## 🔧 Tech Stack
- Python (v3.10 or v3.11 recommended)
- NumPy, Pandas, Scikit-learn
- FastAPI (for backend REST API)
- Streamlit (for interactive frontend)
- joblib/json (for model + threshold persistence)

## 🚀 Features
- Binary classification model to predict loan eligibility
- FastAPI endpoint to serve predictions (`/predict`)
- Streamlit web UI to input features and get predictions
- Clean separation of concerns: model training, API serving, and frontend UI

## 🧠 Model Training
- Supervised learning (e.g., Logistic Regression / Random Forest)
- Data preprocessed and trained using scikit-learn
- Threshold tuned for best F1-score, saved in `threshold.json`

## 🔌 API Endpoint (FastAPI)
Start the API locally:
```bash
uvicorn app.main:app --reload
```

POST /predict: Accepts JSON input and returns predicted label + probability

## Streamlit Web App
Start the frontend:
```bash
  streamlit run app/streamlit_app.py
```
- Simple form-based input UI
- Sends data to the FastAPI backend and shows predictions in real-time

## Setup Instructions:
# Recommended Python 3.10 or 3.11 (scikit-learn does not yet support 3.13)

python -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Run API
uvicorn app.main:app --reload

# In another terminal
streamlit run app/streamlit_app.py


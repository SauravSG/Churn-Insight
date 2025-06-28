#!/bin/bash

# Run FastAPI in background
uvicorn app.main:app --host=0.0.0.0 --port=8000 &

# Run Streamlit (on port 10000 which Render uses)
streamlit run streamlit_app.py --server.port 10000 --server.enableCORS false

# SHL Assessment Recommendation System

A retrieval-based system that recommends SHL individual assessments
based on a natural language query.

## API Endpoints
- GET /health
- POST /recommend

## Run Locally
pip install -r requirements.txt
uvicorn app.main:app --reload

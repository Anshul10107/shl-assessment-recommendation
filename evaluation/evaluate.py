import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000/recommend"

# Load TRAIN sheet
df = pd.read_excel(
    "Gen_AI Dataset.xlsx",
    sheet_name="Train-Set",
    engine="openpyxl"
)

def recall_at_k(predicted, actual, k=10):
    predicted = predicted[:k]
    return len(set(predicted) & set(actual)) / len(actual) if actual else 0

recalls = []

for _, row in df.iterrows():
    query = row["Query"]
    
    # IMPORTANT: Assessment_url may be a single URL per row
    actual_urls = [row["Assessment_url"]]

    response = requests.post(API_URL, json={"query": query})
    predicted_urls = [
        r["url"] for r in response.json()["recommended_assessments"]
    ]

    recalls.append(recall_at_k(predicted_urls, actual_urls, k=10))

print("Mean Recall@10:", round(sum(recalls) / len(recalls), 3))

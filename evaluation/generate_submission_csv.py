import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000/recommend"

test_df = pd.read_excel(
    "Gen_AI Dataset.xlsx",
    sheet_name="Test-Set",
    engine="openpyxl"
)

rows = []

for _, row in test_df.iterrows():
    query = row["Query"]

    response = requests.post(API_URL, json={"query": query})
    urls = [r["url"] for r in response.json()["recommended_assessments"]]

    for url in urls:
        rows.append({
            "Query": query,
            "Assessment_url": url
        })

submission_df = pd.DataFrame(rows)
submission_df.to_csv("evaluation/submission.csv", index=False)

print("submission.csv created successfully")

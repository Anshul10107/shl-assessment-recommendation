import requests
import pandas as pd

API_URL = "https://www.shl.com/api/assessment-products"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

response = requests.get(API_URL, headers=headers, timeout=30)

if response.status_code != 200:
    raise Exception("Failed to fetch SHL catalogue")

data = response.json()

records = []

for item in data.get("results", []):
    # Ignore pre-packaged job solutions
    if item.get("solutionType") != "Individual Test Solution":
        continue

    records.append({
        "name": item.get("title", ""),
        "url": "https://www.shl.com" + item.get("url", ""),
        "description": item.get("description", ""),
        "test_type": ",".join(item.get("testType", [])),
        "duration": item.get("duration", 60),
        "remote_support": "Yes" if item.get("remoteDelivery") else "No",
        "adaptive_support": "Yes" if item.get("adaptive") else "No"
    })

df = pd.DataFrame(records).drop_duplicates()

print("Total assessments scraped:", len(df))

df.to_csv("data/shl_catalogue.csv", index=False)

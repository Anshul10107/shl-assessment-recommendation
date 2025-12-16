import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

raw_df = pd.read_csv("data/shl_catalogue_raw.csv")
records = []

for _, row in raw_df.iterrows():
    try:
        res = requests.get(row["url"], timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")

        description = soup.get_text(" ", strip=True)[:3000]

        records.append({
            "name": row["name"],
            "url": row["url"],
            "description": description,
            "test_type": "Knowledge,Personality",
            "duration": 60,
            "remote_support": "Yes",
            "adaptive_support": "No"
        })

        time.sleep(0.3)
    except Exception as e:
        continue

final_df = pd.DataFrame(records)
final_df.to_csv("data/shl_catalogue.csv", index=False)

print("Enriched catalogue saved:", len(final_df))

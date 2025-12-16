from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="SHL Assessment Recommendation API")

# ---- Lazy-loaded globals ----
df = None
vectorizer = None
tfidf = None


def load_data():
    global df, vectorizer, tfidf

    if df is None:
        df = pd.read_csv("data/shl_catalogue.csv")

        df["combined"] = (
            df["name"].fillna("") + " " +
            df["description"].fillna("") + " " +
            df["test_type"].fillna("")
        )

        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf = vectorizer.fit_transform(df["combined"])


class QueryInput(BaseModel):
    query: str


@app.get("/")
def root():
    return {"message": "SHL Assessment Recommendation API running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/recommend")
def recommend(data: QueryInput):
    load_data()  # 🔥 ONLY loads on first request

    q_vec = vectorizer.transform([data.query])
    scores = cosine_similarity(q_vec, tfidf).flatten()

    df["score"] = scores
    top = df.sort_values("score", ascending=False).head(10)

    results = []
    for _, row in top.iterrows():
        results.append({
            "url": row.get("url"),
            "name": row.get("name"),
            "description": str(row.get("description"))[:500],
            "duration": int(row.get("duration", 0)),
            "adaptive_support": row.get("adaptive_support"),
            "remote_support": row.get("remote_support"),
            "test_type": str(row.get("test_type", "")).split(",")
        })

    return {"recommended_assessments": results}

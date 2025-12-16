from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="SHL Assessment Recommendation API")

df = None
vectorizer = None
tfidf = None


@app.on_event("startup")
def load_model():
    global df, vectorizer, tfidf

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


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/recommend")
def recommend(data: QueryInput):
    q_vec = vectorizer.transform([data.query])
    scores = cosine_similarity(q_vec, tfidf).flatten()

    df["score"] = scores
    top = df.sort_values("score", ascending=False).head(10)

    results = []
    for _, row in top.iterrows():
        results.append({
            "url": row["url"],
            "name": row["name"],
            "description": row["description"][:500],
            "duration": int(row["duration"]),
            "adaptive_support": row["adaptive_support"],
            "remote_support": row["remote_support"],
            "test_type": row["test_type"].split(",")
        })

    return {"recommended_assessments": results}

from fastapi import FastAPI
import pickle
import numpy as np
from textblob import TextBlob

app = FastAPI()


# LOAD MODEL
with open("model/model.pkl", "rb") as f:
    bundle = pickle.load(f)

model = bundle["model"]
scaler = bundle["scaler"]
vectorizer = bundle["vectorizer"]


def get_sentiment(text):
    return TextBlob(text).sentiment.polarity


@app.get("/")
def home():
    return {"message": "API Running"}


@app.post("/predict")
def predict(title: str):
    title_len = len(title)
    word_count = len(title.split())
    sentiment = get_sentiment(title)

    duration = 300
    tags = 10

    text_features = vectorizer.transform([title]).toarray()

    base = np.array([[title_len, word_count, sentiment, duration, tags]])
    X = np.hstack([base, text_features])

    X_scaled = scaler.transform(X)

    pred = model.predict(X_scaled)[0]

    return {
        "prediction": "HIGH" if pred == 1 else "LOW"
    }
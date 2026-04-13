import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer


# ---------------------------
# LOAD DATA
# ---------------------------
def load_data(path="data/14_youtube_video_popularity.csv"):
    print("Running correct pipeline file...")
    df = pd.read_csv(path)
    print("Columns:", df.columns)
    return df


# ---------------------------
# CLEAN DATA
# ---------------------------
def clean_data(df):
    print("Cleaning data...")

    # IMPORTANT: Only use columns that exist
    df = df[['title', 'views', 'duration_sec', 'tags_count']].copy()

    df = df.dropna()
    df = df[df['views'] > 0]

    return df


# ---------------------------
# NLP
# ---------------------------
def get_sentiment(text):
    return TextBlob(str(text)).sentiment.polarity


# ---------------------------
# FEATURE ENGINEERING
# ---------------------------
def feature_engineering(df):
    print("Feature engineering...")

    df['title_len'] = df['title'].apply(len)
    df['word_count'] = df['title'].apply(lambda x: len(str(x).split()))
    df['sentiment'] = df['title'].apply(get_sentiment)

    # Use available dataset columns
    df['duration'] = df['duration_sec']
    df['tags'] = df['tags_count']

    return df


# ---------------------------
# TARGET
# ---------------------------
def create_target(df):
    print("Creating target...")

    threshold = df['views'].quantile(0.75)
    df['success'] = (df['views'] > threshold).astype(int)

    return df


# ---------------------------
# TF-IDF
# ---------------------------
def get_tfidf(df):
    print("Extracting text features...")

    vectorizer = TfidfVectorizer(stop_words='english', max_features=50)
    X_text = vectorizer.fit_transform(df['title'])

    return vectorizer, X_text


# ---------------------------
# TRAIN MODELS
# ---------------------------
def train_models(X_train, y_train, X_test, y_test):
    print("Training models...")

    models = {
        "Logistic": LogisticRegression(max_iter=1000),
        "RandomForest": RandomForestClassifier(),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    }

    best_model = None
    best_score = 0

    for name, model in models.items():
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)

        print(f"\n{name} Accuracy: {score}")
        print(classification_report(y_test, model.predict(X_test)))

        if score > best_score:
            best_score = score
            best_model = model

    return best_model


# ---------------------------
# MAIN
# ---------------------------
def main():
    print("Starting pipeline...")

    df = load_data()
    df = clean_data(df)
    df = feature_engineering(df)
    df = create_target(df)

    vectorizer, X_text = get_tfidf(df)

    base = df[['title_len', 'word_count', 'sentiment', 'duration', 'tags']].values
    X = np.hstack([base, X_text.toarray()])
    y = df['success']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    best_model = train_models(X_train, y_train, X_test, y_test)

    # SAVE MODEL
    bundle = {
        "model": best_model,
        "scaler": scaler,
        "vectorizer": vectorizer
    }

    with open("model/model.pkl", "wb") as f:
        pickle.dump(bundle, f)

    print("Model saved successfully!")
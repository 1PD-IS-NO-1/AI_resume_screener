import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import pickle
import numpy as np

import os  # Add this at the top

def preprocess_data(df):
    # Ensure the "model" directory exists
    os.makedirs("model", exist_ok=True)  # This will create "model" if it doesn’t exist

    # Encode categories (e.g., "Accounting" -> 0, "Engineering" -> 1)
    le = LabelEncoder()
    df['category_encoded'] = le.fit_transform(df['Category'])
    
    # Save the label encoder
    with open("model/label_encoder.pkl", "wb") as f:
        pickle.dump(le, f)
    
    return df

def load_data():
    df = pd.read_csv("Resume/Resume.csv", on_bad_lines="skip") 
    # Handle missing values
    df = df.dropna(subset=['Resume_str', 'Category'])
    return df

def preprocess_data(df):
    # Encode categories (e.g., "Accounting" -> 0, "Engineering" -> 1)
    le = LabelEncoder()
    df['category_encoded'] = le.fit_transform(df['Category'])
    
    # Save the label encoder
    with open("model/label_encoder.pkl", "wb") as f:
        pickle.dump(le, f)
    
    return df

def train_model():
    # Ensure the "model" directory exists BEFORE calling preprocess_data
    os.makedirs("model", exist_ok=True)

    df = load_data()
    df = preprocess_data(df)
    
    # TF-IDF Vectorizer for resume text
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000  # Reduce dimensionality
    )
    #vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['Resume_str'])

    # Save category labels and TF-IDF artifacts
    df[['Category']].drop_duplicates().to_csv("model/categories.csv", index=False)
    pickle.dump(vectorizer, open("model/vectorizer.pkl", "wb"))
    pickle.dump(X, open("model/tfidf_matrix.pkl", "wb"))
    
    # Save artifacts
    
    
    print("Training complete. Model artifacts saved in /model")

if __name__ == "__main__":
    train_model()

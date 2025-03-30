from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# Load dataset and models
try:
    df = pd.read_csv("Resume/Resume.csv")
    df = df.dropna(subset=['Resume_str', 'Category'])
    vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))
    tfidf_matrix = pickle.load(open("model/tfidf_matrix.pkl", "rb"))
except Exception as e:
    raise RuntimeError(f"Failed to load data: {str(e)}")

class ResumeRequest(BaseModel):
    resume_text: str
    desired_category: str

@app.get("/")
def home():
    return {"message": "Resume Screener API"}

@app.get("/categories")
def get_categories():
    """List all available resume categories"""
    try:
        categories = df['Category'].unique().tolist()
        return {
            "available_categories": categories,
            "count": len(categories)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/match")
def match_resume(request: ResumeRequest):
    try:
        # Validate category
        categories = df['Category'].unique().tolist()
        if request.desired_category not in categories:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid category. Available: {categories}"
            )

        # Transform and compare
        input_tfidf = vectorizer.transform([request.resume_text])
        category_mask = df['Category'] == request.desired_category
        category_tfidf = tfidf_matrix[category_mask]
        similarity = cosine_similarity(input_tfidf, category_tfidf)
        
        return {
            "match_score": float(np.mean(similarity)),
            "category": request.desired_category,
            "samples_matched": sum(category_mask)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
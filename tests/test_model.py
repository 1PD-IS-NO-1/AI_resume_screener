import pytest
import pickle
import pandas as pd

def test_model_loading():
    try:
        with open("model/tfidf_vectorizer.pkl", "rb") as f:
            vectorizer = pickle.load(f)
        assert hasattr(vectorizer, "transform"), "Vectorizer missing transform method"
        
        mappings = pd.read_csv("model/category_mappings.csv")
        assert "Category" in mappings.columns, "Missing category column"
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")
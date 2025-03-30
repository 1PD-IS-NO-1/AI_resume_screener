import streamlit as st
import requests
import os

# Configure backend URL - critical fix!
BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:8000')  # Docker internal networking

st.set_page_config(page_title="Resume Screener", layout="wide")

# Error handling decorator
def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Backend service unavailable. Please try again later.")
            st.stop()
    return wrapper

@handle_errors
def get_categories():
    return requests.get(f"{BACKEND_URL}/categories").json()

@handle_errors
def match_resume(resume_text, category):
    return requests.post(
        f"{BACKEND_URL}/match",
        json={"resume_text": resume_text, "desired_category": category}
    )

# UI Components
st.title("📄 AI Resume Screener")
st.markdown("Analyze how well your resume matches different job categories")

try:
    categories_data = get_categories()
    categories = categories_data["available_categories"]
    
    with st.form("resume_form"):
        col1, col2 = st.columns(2)
        with col1:
            resume_text = st.text_area("Paste your resume text:", height=300)
        with col2:
            desired_category = st.selectbox("Target category:", categories)
            submitted = st.form_submit_button("Analyze Resume")

    if submitted:
        if not resume_text.strip():
            st.warning("Please enter resume text")
        else:
            with st.spinner("Analyzing..."):
                response = match_resume(resume_text, desired_category)
                
            if response.status_code == 200:
                result = response.json()
                st.success(f"Match Score: {result['match_score']:.2f}/1.0")
                
                # Visual feedback
                progress = result['match_score']
                st.progress(progress)
                
                col1, col2 = st.columns(2)
                col1.metric("Category", result['category'])
                col2.metric("Compared With", f"{result['samples_matched']} resumes")
                
            else:
                st.error(f"Analysis failed: {response.json().get('detail', 'Unknown error')}")

except Exception as e:
    st.error(f"Application error: {str(e)}")
    st.stop()
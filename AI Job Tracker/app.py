import os
import re
import streamlit as st
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# --- HELPER FUNCTIONS ---

def extract_text_from_pdf(pdf_file) -> str:
    """Extracts text content from an uploaded PDF file."""
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + " "
    return text

def clean_text(text: str) -> str:
    """Normalizes text by lowercasing and removing special characters."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_match_score(resume_text: str, jd_text: str):
    """Calculates TF-IDF Cosine Similarity between resume and job description."""
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(jd_text)
    
    corpus = [cleaned_resume, cleaned_jd]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    match_percentage = round(similarity_matrix[0][0] * 100, 2)
    
    return match_percentage, vectorizer

def get_missing_keywords(resume_text: str, jd_text: str, vectorizer) -> list:
    """Identifies top keywords in the JD that are absent from the resume."""
    cleaned_resume = set(clean_text(resume_text).split())
    feature_names = set(vectorizer.get_feature_names_out())
    
    jd_words = set(clean_text(jd_text).split()).intersection(feature_names)
    missing_words = [word for word in jd_words if word not in cleaned_resume]
    
    return sorted(missing_words)[:10]

def generate_ai_bullet_points(jd_text: str, resume_text: str, missing_keywords: list) -> str:
    """Uses Gemini API to generate resume bullet points covering missing keywords."""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        return "⚠️ **Error:** `GEMINI_API_KEY` not found in `.env` file. Please check your `.env` configuration."
    
    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are an expert resume writer and HR consultant.
        
        A candidate is applying for a job with this description:
        ---
        {jd_text[:1500]}
        ---
        
        The candidate's current resume content is:
        ---
        {resume_text[:1500]}
        ---
        
        The following essential keywords are missing from their resume:
        {', '.join(missing_keywords)}
        
        Task: Write 3 to 5 professional, high-impact resume bullet points (using the Google/XYZ formula: "Accomplished [X] as measured by [Y], by doing [Z]").
        Ensure that you naturally integrate the missing keywords into these bullet points.
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        
        return response.text

    except Exception as e:
        return f"⚠️ **API Error:** {str(e)}"

# --- STREAMLIT UI ---

st.set_page_config(page_title="AI Resume Optimizer", page_icon="📄", layout="wide")

st.title("🤖 AI Resume Matcher & Content Rewriter")
st.markdown("Calculate match scores, find missing skill gaps, and generate tailored bullet points using Gemini AI.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Job Description")
    jd_input = st.text_area("Paste the job posting here:", height=250, placeholder="Requirements: Python, SQL, Machine Learning, Streamlit...")

with col2:
    st.subheader("2. Candidate Resume")
    uploaded_pdf = st.file_uploader("Upload PDF Resume:", type=["pdf"])

if st.button("🚀 Analyze & Rewrite", use_container_width=True):
    if not jd_input.strip() or not uploaded_pdf:
        st.warning("Please provide both a Job Description and upload a PDF Resume.")
    else:
        with st.spinner("Extracting text and calculating match score..."):
            resume_text = extract_text_from_pdf(uploaded_pdf)
            
            if not resume_text.strip():
                st.error("Could not extract readable text from the uploaded PDF.")
            else:
                score, vectorizer = calculate_match_score(resume_text, jd_input)
                missing_keywords = get_missing_keywords(resume_text, jd_input, vectorizer)
                
                st.markdown("---")
                st.header("Match Analysis")
                
                # Display Match Score
                st.metric(label="Overall Match Score", value=f"{score}%")
                
                if score >= 70:
                    st.success("🔥 High Match! Your resume aligns well with this job.")
                elif score >= 45:
                    st.info("💡 Moderate Match. Consider tailoring key missing terms.")
                else:
                    st.error("⚠️ Low Match. Crucial skills from the job description are missing.")
                
                # Display Missing Keywords
                st.subheader("🔑 Missing Keywords")
                if missing_keywords:
                    st.write(", ".join([f"`{kw}`" for kw in missing_keywords]))
                    
                    # Generate AI Bullet Points
                    st.subheader("✨ AI Recommended Resume Bullet Points")
                    with st.spinner("Generating bullet points via Gemini AI..."):
                        ai_suggestions = generate_ai_bullet_points(jd_input, resume_text, missing_keywords)
                        st.markdown(ai_suggestions)
                else:
                    st.success("No major keywords missing from your resume!")
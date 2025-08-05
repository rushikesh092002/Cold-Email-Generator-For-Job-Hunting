import os
import streamlit as st
from dotenv import load_dotenv
from extarctors.resune_extractor import extract_text_from_pdf, extract_text_from_docx, extract_education_experience
from llm_services.cover_letter import generate_cover_letter
from llm_services.job_analysis import analyze_job_description
from utils.file_handler import save_uploaded_file
from utils.linkdin_scraper import scrape_linkdin_job_details
from utils.email_sender import send_email

# Load environment variables
load_dotenv()

# Streamlit Setup
st.set_page_config(page_title="AI Cover Letter Generator", layout="centered")
st.title("📄 AI Cover Letter & One-Click Apply")

# Session State Initialization
for key in ["resume_text", "job_details", "education", "experience", "file_path"]:
    if key not in st.session_state:
        st.session_state[key] = None if key == "resume_text" or key == "file_path" else {}

# Upload Resume
uploaded_file = st.file_uploader("📂 Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
if uploaded_file:
    st.session_state.file_path = save_uploaded_file(uploaded_file)
    extractor = extract_text_from_pdf if uploaded_file.name.endswith(".pdf") else extract_text_from_docx
    st.session_state.resume_text = extractor(st.session_state.file_path)
    st.session_state.education, st.session_state.experience = extract_education_experience(st.session_state.resume_text)
    st.success("✅ Resume uploaded successfully!")

# LinkedIn Job Scraper
job_url = st.text_input("🔗 LinkedIn Job URL")
if st.button("🔍 Auto-Fill Job Details") and job_url:
    job_details = scrape_linkdin_job_details(job_url)
    if isinstance(job_details, dict):
        st.session_state.job_details = job_details
        st.subheader("📌 Job Details:")
        for key in ["title", "company", "location", "job_description"]:
            st.write(f"**{key.capitalize()}:** {job_details.get(key, 'N/A')}")
    else:
        st.error("⚠️ Failed to retrieve job details.")

# Analyze Job Description
if st.session_state.job_details:
    st.subheader("📊 Job Analysis:")
    st.write(analyze_job_description(st.session_state.job_details.get("job_description", "")))

# Generate & Send Email
recipient_email = st.text_input("📧 Hiring Manager's Email")
if st.button("📨 Apply via Email") and st.session_state.resume_text and recipient_email:
    job_title = st.session_state.job_details.get("title", "a relevant position")
    company_name = st.session_state.job_details.get("company", "your esteemed organization")

    email_body = generate_cover_letter("Rushikesh Gaikhe", job_title, company_name, st.session_state.resume_text, 
                                       st.session_state.job_details.get("job_description", "No job description provided."))

    if st.session_state.file_path:  # Ensure the file exists before sending
        send_email(recipient_email, f"Application for {job_title} at {company_name}", email_body, st.session_state.file_path)
        st.success("✅ Email sent successfully!")
    else:
        st.error("⚠️ Resume file not found. Please upload a resume.")

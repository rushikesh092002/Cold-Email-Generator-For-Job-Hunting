import PyPDF2
import docx
import re

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path , "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text.strip() or "No readable text found."
    except Exception as e:
        return f"Error extracting text: {str(e)}"


def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip() or "No readble text found."
    except Exception as e:
        return f"Error Extracting Text: {str(e)}"
    


def extract_education_experience(resume_text):
    education_pattern = re.findall(r"(B\.?Tech|M\.?Tech|Bachelor|Master|PhD|Diploma|BSc|MSc)[^\n]+", resume_text, re.IGNORECASE)
    experience_pattern = re.findall(r"(\d+ years?|\d+ months?) of experience", resume_text , re.IGNORECASE)

    education = ", ".join(education_pattern) if education_pattern else "Not Found"
    experience =", ".join(experience_pattern) if  experience_pattern else "Not Found"

    return education, experience 
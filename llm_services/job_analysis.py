from langchain_groq import ChatGroq
from config.config  import GROQ_API_KEY, MODEL_NAME


llm = ChatGroq(model= MODEL_NAME, api_key = GROQ_API_KEY)

def analyze_job_description(job_description):
    prompt = f"""
    Analyze the following job description and extract:
    - Key skills required
    - Main responsibilities
    - Preferred qualifications
    - Any special requirements

    Job Description:
    {job_description}

    Return the analysis in a structured format.
    """
    return llm.invoke(prompt).content
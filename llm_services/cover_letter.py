from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY, MODEL_NAME

llm = ChatGroq(model=MODEL_NAME ,api_key=GROQ_API_KEY)

cover_letter_prompt = PromptTemplate(
    input_variables=["name", "role", "company", "resume", "job_description"],
    template="""Write a professional cover letter for {name} applying for the {role} position at {company}.
    Use the following resume details: {resume}
    Consider the job description: {job_description}
    Make it formal, engaging, and aligned with industry standards. but in short direct give information """
)


def generate_cover_letter(name, role, company, resume_text, job_description):
    formatted_prompt = cover_letter_prompt.format(
        name=name, role=role, company=company, resume=resume_text, job_description=job_description
    )
    response = llm.invoke(formatted_prompt)
    return response.content if hasattr(response, "content") else str(response)

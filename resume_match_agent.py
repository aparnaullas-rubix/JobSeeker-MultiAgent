from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os

llm = AzureChatOpenAI(
    azure_endpoint="https://iz-genai-polarion-openai.openai.azure.com/",
    api_version="2024-08-01-preview",
    deployment_name="gpt-4o-mini"
)

def rate_resume_against_job(resume_text: str, job_text: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a job matching assistant that scores resumes."),
        ("human", 
         f"""
Compare the following resume and job posting.

Resume:
{resume_text}

Job Posting:
{job_text}

Give:
- A match score out of 100
- 2–3 reasons why the score is what it is
"""
        )
    ])
    chain = prompt | llm
    result = chain.invoke({})
    return result.content.strip()
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
import os

# Load your Azure model
llm = AzureChatOpenAI(
    azure_endpoint="https://iz-genai-polarion-openai.openai.azure.com/",
    api_version="2024-08-01-preview",
    deployment_name="gpt-4o-mini"
)

def suggest_resume_improvements(resume_text: str, ats_keywords: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert resume coach who specializes in ATS optimization."),
        ("human", 
         f"""Here is a resume:\n\n{resume_text}\n\n
         And here is a list of extracted ATS keywords:\n\n{ats_keywords}\n\n
         1. Identify which important keywords are **missing** in the resume.
         2. Suggest **bullet points or short phrases** that could be added to include those missing keywords.
         3. Do not rewrite the whole resume. Only return a list of suggestions.
         """)
    ])
    chain = prompt | llm
    result = chain.invoke({})
    return result.content.strip()
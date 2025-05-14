from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import AzureChatOpenAI
from langchain.tools import Tool
import os

# Load your Azure LLM
llm = AzureChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint="https://iz-genai-polarion-openai.openai.azure.com/",
    api_version="2024-08-01-preview",
    deployment_name="gpt-4o-mini"
)

def extract_ats_keywords(job_posting: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an ATS optimization assistant."),
        ("human", 
         f"""Extract the most relevant keywords from the following job listing. 
         Include skills, tools, technologies, qualifications, and common action verbs that should appear on a resume.
         
         Job Listing:
         {job_posting}

         Return the keywords as a comma-separated list."""
        )
    ])
    chain = prompt | llm
    result = chain.invoke({})
    return result.content.strip()

ats_keyword_tool = Tool(
    name="extract_ats_keywords",
    func=extract_ats_keywords,
    description="Extract ATS-relevant keywords from a job posting"
)
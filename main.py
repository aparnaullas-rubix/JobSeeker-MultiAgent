from dotenv import load_dotenv
import os
from resume_utils import extract_text_from_pdf
from job_search_agent import search_jobs_from_resume
from ats_keyword_agent import extract_ats_keywords
from tools import save_to_txt
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from resume_match_agent import rate_resume_against_job

# --- Load Environment Variables ---
load_dotenv()

# --- 1. Extract Resume Text ---
resume_path = ""  # Update to your actual file path
resume_text = extract_text_from_pdf(resume_path)

# --- 2. Job Search ---
print("\n🔍 Searching for jobs based on your resume...\n")
job_results = search_jobs_from_resume(resume_text)
print(job_results)

# --- 3. Extract ATS Keywords ---
print("\n🧠 Extracting ATS keywords...\n")
ats_keywords = extract_ats_keywords(job_results)
print("🔑 ATS Keywords:", ats_keywords)

# --- 4. Rate Resume Against Job ---
print("\n📊 Rating your resume against a job posting...\n")

# Optionally pick the first job (most detailed)
first_job_snippet = job_results.split("🔹")[1] if "🔹" in job_results else job_results
match_rating = rate_resume_against_job(resume_text, first_job_snippet)

print(match_rating)

# --- 5. Suggest Resume Bullet Improvements ---
print("\n✍️ Generating resume improvement suggestions...\n")

llm = AzureChatOpenAI(
    azure_endpoint="https://iz-genai-polarion-openai.openai.azure.com/",
    api_version="2024-08-01-preview",
    deployment_name="gpt-4o-mini"
)

resume_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a resume optimization assistant."),
    ("human", 
     f"""The following resume was provided:

{resume_text}

The following are important keywords from current job listings:

{ats_keywords}

Based on this, suggest bullet points, skills, or phrasing the user should consider adding or revising in their resume to improve matching with ATS. Return 5-7 concrete suggestions."""
    )
])

chain = resume_prompt | llm
resume_suggestions = chain.invoke({}).content.strip()
print(resume_suggestions)

# --- 6. Save Output ---
print("\n💾 Saving everything to job_search_results.txt...\n")
save_to_txt(
    f"{job_results}\n\n🔑 ATS Keywords:\n{ats_keywords}\n\n✍️ Resume Suggestions:\n{resume_suggestions}\n\n📊 Match Rating:\n{match_rating}",
    filename="job_search_results.txt"
)

print("✅ Done! Results saved to job_search_results.txt")

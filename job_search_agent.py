from langchain.tools import Tool
import requests
import os

GERMAN_HUBS = ["Remote", "Hybrid", "Erlangen", "Nuremberg", "Fürth", "Bamberg", "Munich"]

def search_jobs_from_resume(resume_text: str, location_keywords=GERMAN_HUBS) -> str:
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("Missing SERPER_API_KEY")

    # Infer probable job title from resume (simplified here)
    role_guess = " ".join([
        word for word in resume_text.split() if word.lower() in
        ["data", "scientist", "engineer", "ai", "ml", "research", "developer"]
    ]) or "Software Engineer"

    # Create search query
    query = f"{role_guess} jobs in Germany ({' OR '.join(location_keywords)}) site:linkedin.com/jobs OR site:indeed.com"
    
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
    data = {"q": query}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    results = response.json().get("organic", [])

    if not results:
        return "No jobs found."

    output = []
    for r in results[:5]:  # Limit to top 5 jobs
        title = r.get("title")
        link = r.get("link")
        snippet = r.get("snippet", "")
        output.append(f"🔹 {title}\n{snippet}\n🔗 {link}\n")

    return "\n".join(output)

job_search_tool = Tool(
    name="job_search_from_resume",
    func=search_jobs_from_resume,
    description="Given resume text, search for matching jobs in Germany (remote, hybrid, or specific cities)."
)
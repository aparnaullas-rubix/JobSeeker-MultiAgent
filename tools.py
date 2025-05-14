from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
from langchain.tools import Tool
import os
import requests


def save_to_txt(data: str, filename: str="research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data sucessfully saved to {filename}"
save_tool = Tool(
    name = "save_text_to_file",
    func=save_to_txt,
    description="Save structured research data to a text file.",
)

def serper_search(query: str) -> str:
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("SERPER_API_KEY not set in environment.")

    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
    data = {"q": query}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    results = response.json()

    output = []
    for item in results.get("organic", [])[:3]:  # Limit to top 3 results
        output.append(f"- {item.get('title')} ({item.get('link')})\n  {item.get('snippet')}")
    
    return "\n".join(output) or "No results found."

serper_tool = Tool(
    name="serper",
    func=serper_search,
    description="Search the web using Serper.dev (Google Search API).",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
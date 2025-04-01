import asyncio
import os
import platform
import getpass
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig
from dotenv import load_dotenv

load_dotenv() 
api_key = os.getenv("GOOGLE_API_KEY")
# Initialize FastAPI
app = FastAPI()
# Set Google API Key

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Set Chrome path based on OS
if platform.system() == "Windows":
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
elif platform.system() == "Linux":
    chrome_path = "/usr/bin/google-chrome"
else:
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Initialize browser instance
browser = Browser(config=BrowserConfig(headless=False, disable_security=False, chrome_instance_path=chrome_path))

# Define request model
class SearchRequest(BaseModel):
    query: str  # Search term

@app.get("/")
def home():
    return {"message": "FastAPI is running!"}

@app.post("/search/")
async def run_browser_task(request: SearchRequest):
    """
    Trigger the browser automation task based on the user-provided search term.
    """
    task_description = f"""
        Perform the following task '{request.query}'.
    """

    agent = Agent(task=task_description, llm=llm, browser=browser)
    await agent.run()
    
    return {"status": "Task Completed", "search_term": request.query}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)


from src.agent import BrowserAgent
import asyncio

async def web_search_and_scrape(query: str, provider: str = "gemini"):
    """
    Workflow to search a query and scrape top results.
    """
    print(f"Starting workflow: Web Search & Scrape for '{query}'")
    task_description = (
        f"Search the web for '{query}'. "
        "Extract the top 5 results with their Title, URL, and a brief description. "
        "Return the data as a JSON object."
    )
    agent = BrowserAgent(description=task_description, provider=provider)
    await agent.run()

async def table_scraper(url: str, provider: str = "gemini"):
    """
    Workflow to scrape a table from a given URL.
    """
    print(f"Starting workflow: Table Scraper for {url}")
    task_description = (
        f"Navigate to '{url}'. "
        "Find the main data table on the page. "
        "Extract all rows and columns. "
        "Save the data as a CSV file in the current working directory or the run directory."
    )
    agent = BrowserAgent(description=task_description, provider=provider)
    await agent.run()

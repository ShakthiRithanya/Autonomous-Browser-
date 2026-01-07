
import argparse
import asyncio
import sys

# Force UTF-8 output to prevent Windows emoji crashes
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
from src.agent import BrowserAgent
from src.workflows import web_search_and_scrape, table_scraper

async def main():
    parser = argparse.ArgumentParser(description="Autonomous Browser Agent")
    parser.add_argument("--task", type=str, help="The natural language task to perform")
    parser.add_argument("--provider", type=str, default="gemini", choices=["gemini", "openai"], help="LLM Provider")
    parser.add_argument("--demo", type=str, choices=["github", "news", "table"], help="Run a demo scenario")
    parser.add_argument("--url", type=str, help="URL for table scraper demo")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompt")
    
    args = parser.parse_args()

    task_description = args.task
    
    # Handle Demos
    if args.demo:
        if args.demo == "github":
            task_description = "Open the browser-use GitHub repo (https://github.com/browser-use/browser-use) and tell me its current star count."
        elif args.demo == "news":
            task_description = "Search the web for latest articles about 'Google Antigravity' and summarize the top 5 in bullet points with links."
        elif args.demo == "table":
            if not args.url:
                # Default to a generic table page if not provided, or ask user.
                # Let's use a known stable one or search for one.
                # We'll default to a simple example if none provided.
                task_description = "Go to https://www.w3schools.com/html/html_tables.asp, scrape the 'Customers' table into a CSV."
            else:
                task_description = f"Go to {args.url}, find the main table, scrape it into CSV."
    
    # Interactive mode if no task provided
    if not task_description:
        print("Welcome to the Autonomous Browser Agent!")
        task_description = input("Please enter your task description: ").strip()
        if not task_description:
            print("No task provided. Exiting.")
            return

    # Echo and Validate
    print("\n--- Task Configuration ---")
    print(f"Task: {task_description}")
    print(f"Provider: {args.provider}")
    print("--------------------------\n")
    
    if not args.yes:
        confirm = input("Proceed? (y/n): ").lower()
        if confirm != 'y':
            print("Aborted.")
            return

    # Execution
    try:
        agent = BrowserAgent(description=task_description, provider=args.provider)
        await agent.run()
        print("\nTask completed successfully.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())

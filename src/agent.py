
import asyncio
import os
import json
from datetime import datetime
from browser_use import Agent, Browser, Controller
from langchain_core.messages import HumanMessage, SystemMessage
from src.config import get_llm

class BrowserAgent:
    def __init__(self, description: str, provider: str = "gemini", max_steps: int = 100):
        self.description = description
        self.llm = get_llm(provider)
        self.max_steps = max_steps
        
        # Create runs directory
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_dir = os.path.join(os.getcwd(), "runs", self.timestamp)
        os.makedirs(self.run_dir, exist_ok=True)
        
        # Setup specific system prompt as requested
        self.system_prompt = (
            "You are an autonomous web automation agent. You can control a real browser via tools. "
            "Plan before you act, explain your reasoning briefly, then choose actions "
            "(navigate, click, type, scroll, extract) until the task is done or you hit safety limits."
        )

    async def run(self):
        """
        Runs the agent with the given task.
        """
        # Explicit config
        try:
             from browser_use import BrowserConfig
             config = BrowserConfig(headless=False)
             browser = Browser(config=config)
        except ImportError:
             # fallback for older versions or if import fails
             browser = Browser()
        
        # We can pass the system prompt if the library allows, or prepend it to the task.
        # browser-use Agent typically takes 'task' and 'llm'. 
        # We'll prepend the system instruction to the task to be safe, 
        # or use 'system_prompt' kwarg if available (it often is in newer versions).
        # We'll stick to a robust approach: Task + Instruction.
        
        # Patch for browser-use 0.11+ which might check .provider on the LLM object
        if not hasattr(self.llm, "provider"):
             # infer provider
             if "google" in str(type(self.llm)).lower():
                self.llm.provider = "google"
             elif "openai" in str(type(self.llm)).lower():
                 self.llm.provider = "openai"
             else:
                 self.llm.provider = "unknown"

        full_task = f"{self.system_prompt}\n\nTask: {self.description}"

        agent = Agent(
            task=full_task,
            llm=self.llm,
            browser=browser,
            use_vision=False, # Disabled for rate limits
            save_conversation_path=os.path.join(self.run_dir, "conversation.json")
        )
        
        print(f"🚀 Starting task: {self.description}")
        print(f"📂 Run directory: {self.run_dir}")

        try:
            history = await agent.run(max_steps=self.max_steps)
            # Save artifacts
            self.save_history(history)
            return history
        finally:
            # Clean up
            if hasattr(browser, 'close'):
                await browser.close()
            else:
                 print(f"Browser object has no close method. Type: {type(browser)}")
                 print(f"Dir: {dir(browser)}")

    def save_history(self, history):
        history_path = os.path.join(self.run_dir, "history.json")
        try:
            # history might be an object, need to ensure it's serializable
            # If it's a list StepResult, we convert to dict
            if hasattr(history, "to_json"):
                with open(history_path, "w", encoding='utf-8') as f:
                    f.write(history.to_json())
            else:
                 with open(history_path, "w", encoding='utf-8') as f:
                    f.write(str(history))
        except Exception as e:
            print(f"Error saving history: {e}")

        # Task Report
        report_path = os.path.join(self.run_dir, "report.md")
        with open(report_path, "w", encoding='utf-8') as f:
            f.write(f"# Task Report\n\n")
            f.write(f"**Task:** {self.description}\n")
            f.write(f"**Timestamp:** {self.timestamp}\n\n")
            f.write(f"## Summary\n")
            f.write(f"Task completed. Check artifacts for details.\n")
            

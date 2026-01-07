
import asyncio
import logging
import os
import traceback
from typing import Callable, Optional
from datetime import datetime
from src.config import get_llm

try:
    from browser_use import Agent, Browser, BrowserConfig
except ImportError:
    from browser_use import Agent, Browser
    try:
        from browser_use.browser.browser import BrowserConfig
    except ImportError:
        BrowserConfig = None

logger = logging.getLogger("browser_use")

class StreamBrowserAgent:
    def __init__(self, description: str, provider: str = "gemini", max_steps: int = 50, output_callback: Optional[Callable[[str], None]] = None):
        self.description = description
        self.llm = get_llm(provider)
        self.max_steps = max_steps
        self.output_callback = output_callback
        
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_dir = os.path.join(os.getcwd(), "runs", self.timestamp)
        os.makedirs(self.run_dir, exist_ok=True)
        
        self.system_prompt = (
            "You are an autonomous web automation agent. "
            "Plan tasks step-by-step. "
        )

    async def run(self):
        browser = None
        try:
             # Try explicit config
             if BrowserConfig:
                 config = BrowserConfig(headless=False, disable_security=True)
                 browser = Browser(config=config)
             else:
                 browser = Browser()
        except Exception as e:
             if self.output_callback:
                 self.output_callback(f"⚠️ Config Warning: {e}, using default Browser()")
             browser = Browser()

        # Patch LLM provider if needed
        if not hasattr(self.llm, "provider"):
             name = str(type(self.llm)).lower()
             if "google" in name: self.llm.provider = "google"
             elif "openai" in name: self.llm.provider = "openai"
             else: self.llm.provider = "unknown"

        full_task = f"{self.system_prompt}\n\nTask: {self.description}"
        
        if self.output_callback:
            self.output_callback(f"🚀 Initializing Agent for task: {self.description}")
            self.output_callback(f"⚠️ Note: Vision disabled to prevent API rate limits.")
            self.output_callback(f"📂 Saving runs to: {self.run_dir}")

        agent = Agent(
            task=full_task,
            llm=self.llm,
            browser=browser,
            use_vision=False, 
            save_conversation_path=os.path.join(self.run_dir, "conversation.json")
        )

        try:
            if self.output_callback:
                self.output_callback("🤖 Agent starting... (check browser window)")
            
            history = await agent.run(max_steps=self.max_steps)
            
            if self.output_callback:
                self.output_callback("✅ Task complete!")
            
            self.save_artifacts(history)
            return history
            
        except Exception as e:
            tb = traceback.format_exc()
            if self.output_callback:
                self.output_callback(f"❌ Error: {str(e)}\nTraceback:\n{tb}")
            print(f"Server Error: {e}")
            print(tb)
            raise e
        finally:
            if browser and hasattr(browser, 'close'):
                await browser.close()
            else:
                 pass 

    def save_artifacts(self, history):
        path = os.path.join(self.run_dir, "history.json")
        try:
            with open(path, "w", encoding='utf-8') as f:
                if hasattr(history, "to_json"):
                    f.write(history.to_json())
                else:
                    f.write(str(history))
        except Exception:
            pass


import os
from dotenv import load_dotenv
# Use browser_use built-in LLM wrappers which likely have 'provider' etc.
try:
    from browser_use.llm import ChatGoogle, ChatOpenAI
except ImportError:
    # Fallback or error if these are missing, but we verified they exist.
    from langchain_google_genai import ChatGoogleGenerativeAI as ChatGoogle
    from langchain_openai import ChatOpenAI

load_dotenv()

def get_llm(provider: str = "gemini"):
    """
    Returns the LLM instance based on the provider.
    """
    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
        # browser-use ChatGoogle likely uses GOOGLE_API_KEY env var standard
        os.environ["GOOGLE_API_KEY"] = api_key
        
        # Use gemini-2.0-flash-exp or gemini-pro (supported models)
        return ChatGoogle(model="gemini-2.0-flash-exp", api_key=api_key)
        
    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        return ChatOpenAI(model="gpt-4o", api_key=api_key)
    else:
        raise ValueError(f"Unknown provider: {provider}")

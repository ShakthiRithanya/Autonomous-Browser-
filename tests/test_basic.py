
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from src.agent import BrowserAgent
from src.workflows import web_search_and_scrape

@pytest.mark.asyncio
async def test_agent_initialization():
    with patch("src.agent.get_llm") as mock_get_llm:
        agent = BrowserAgent("Test task")
        assert agent.description == "Test task"
        assert agent.run_dir is not None

@pytest.mark.asyncio
async def test_workflow_execution():
    with patch("src.workflows.BrowserAgent") as MockAgent:
        mock_instance = MockAgent.return_value
        mock_instance.run = AsyncMock()
        
        await web_search_and_scrape("test query")
        
        MockAgent.assert_called_once()
        mock_instance.run.assert_called_once()

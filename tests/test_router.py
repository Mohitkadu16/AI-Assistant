import pytest
# pyrefly: ignore [missing-import]
from src.agents.router_agent import RouterAgent
# pyrefly: ignore [missing-import]
from src.agents.base_agent import BaseAgent
# pyrefly: ignore [missing-import]
from typing import Any, Dict, Optional

class MockAgent(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name=name, description="A mock agent for testing.")

    def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        return f"Mock {self.name} processed: {task}"

def test_router_agent_registration():
    router = RouterAgent()
    mock_agent = MockAgent(name="Test Agent")
    
    router.register_agent(mock_agent)
    
    assert "Test Agent" in router.registered_agents
    assert router.registered_agents["Test Agent"] == mock_agent

def test_router_agent_routing():
    router = RouterAgent()
    mock_agent = MockAgent(name="Test Agent")
    router.register_agent(mock_agent)
    
    result = router.process_task("Some random task")
    assert result == "Mock Test Agent processed: Some random task"

def test_router_no_agents():
    router = RouterAgent()
    with pytest.raises(ValueError, match="No specialized agents registered to handle tasks."):
        router.process_task("Some task")

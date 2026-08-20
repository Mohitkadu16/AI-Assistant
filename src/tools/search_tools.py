from typing import Any
from src.tools.base_tool import BaseTool

class WebSearchTool(BaseTool):
    def __init__(self):
        super().__init__(name="Web Search", description="Searches the web for current information.")

    def execute(self, query: str, **kwargs) -> Any:
        # Stub implementation
        return f"Stub: Searched web for '{query}'"

class GitHubTool(BaseTool):
    def __init__(self):
        super().__init__(name="GitHub", description="Interacts with GitHub repositories.")

    def execute(self, action: str, repo: str, **kwargs) -> Any:
        # Stub implementation
        return f"Stub: Performed {action} on {repo}"

from typing import Any, Dict, Optional
from src.agents.base_agent import BaseAgent
from src.tools.llm_tools import OllamaTool

class ChatAgent(BaseAgent):
    """
    Responsibilities:
    * Handle casual conversation
    * Provide quick, general answers
    * Be friendly and conversational
    """
    def __init__(self) -> None:
        super().__init__(name="General Chat Agent", description="Handles general casual conversation and quick answers.")
        self.system_prompt = "You are a helpful, friendly General Chat Agent. Provide concise and conversational responses without unnecessary technical jargon."
        self.llm = OllamaTool(model_name="qwen3")

from typing import Any, Dict, Optional
from src.agents.base_agent import BaseAgent
from src.configs.prompt_loader import PromptLoader
from src.tools.llm_tools import OllamaTool

class PhotographyAgent(BaseAgent):
    """
    Responsibilities:
    * Composition advice, Lightroom workflow, Color grading
    * Portfolio review, Caption suggestions, Creative feedback
    """
    def __init__(self) -> None:
        super().__init__(name="Photography Agent", description="Assistant for photography and color grading.")
        self.system_prompt = PromptLoader.get_prompt("photography")
        self.llm = OllamaTool(model_name="qwen3")

    def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        history = context.get("history", []) if context else []
        history_str = ""
        for msg in history[-5:]:  # Include last 5 messages for context
            role = "User" if msg["is_user"] else "AI"
            history_str += f"{role}: {msg['content']}\n"
            
        full_prompt = task
        if history_str:
            full_prompt = f"Previous Conversation Context:\n{history_str}\n\nCurrent Request: {task}"
            
        response = self.llm.execute(prompt=full_prompt, system=self.system_prompt)
        return {"status": "success", "agent": self.name, "result": response}

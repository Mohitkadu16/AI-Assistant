from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from src.utils.logger import logger

class BaseAgent(ABC):
    """
    Abstract Base Class for all agents following SOLID principles.
    Provides the core contract that any agent must fulfill.
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        logger.debug(f"Initialized agent: {self.name}")

    def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Standard synchronous processing of a task.
        """
        history = context.get("history", []) if context else []
        history_str = ""
        for msg in history[-5:]:
            role = "User" if msg["is_user"] else "AI"
            history_str += f"{role}: {msg['content']}\n"
            
        full_task = task
        if history_str:
            full_task = f"Previous Conversation Context:\n{history_str}\n\nCurrent Request: {task}"
            
        images = context.get("images", []) if context else []
        response = self.llm.execute(prompt=full_task, system=self.system_prompt, images=images)
        return {"status": "success", "agent": self.name, "result": response}

    def process_task_stream(self, task: str, context: Optional[Dict[str, Any]] = None):
        """
        Generator that streams tokens for a task.
        """
        history = context.get("history", []) if context else []
        history_str = ""
        for msg in history[-5:]:
            role = "User" if msg["is_user"] else "AI"
            history_str += f"{role}: {msg['content']}\n"
            
        full_prompt = task
        if history_str:
            full_prompt = f"Previous Conversation Context:\n{history_str}\n\nCurrent Request: {task}"
            
        for chunk in self.llm.stream_execute(prompt=full_prompt, system=self.system_prompt):
            yield chunk

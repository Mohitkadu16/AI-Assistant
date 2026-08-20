from typing import Any, Dict, List, Optional
# pyrefly: ignore [missing-import]
from src.agents.base_agent import BaseAgent
# pyrefly: ignore [missing-import]
from src.utils.logger import logger
from src.tools.llm_tools import OllamaTool

class RouterAgent(BaseAgent):
    """
    Master Router Agent.
    Responsible for analyzing user intent and delegating the task to the correct specialized agent.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Master Router Agent",
            description="Analyzes input and routes to specialized agents."
        )
        self.registered_agents: Dict[str, BaseAgent] = {}
        self.llm = OllamaTool(model_name="qwen3")

    def register_agent(self, agent: BaseAgent) -> None:
        """
        Registers a specialized agent with the router.
        """
        self.registered_agents[agent.name] = agent
        logger.info(f"Registered specialized agent: {agent.name}")

    def route(self, task: str) -> BaseAgent:
        """
        Analyzes the task and determines which agent should handle it using Ollama.
        """
        logger.debug(f"Routing task: '{task}'")
        if not self.registered_agents:
            raise ValueError("No specialized agents registered to handle tasks.")
        
        agent_descriptions = "\n".join([f"- '{name}': {agent.description}" for name, agent in self.registered_agents.items()])
        
        system_prompt = f"""You are a Master Router Agent. Your job is to classify the user's task and delegate it to the MOST appropriate specialized agent.
Available Agents:
{agent_descriptions}

You must reply with ONLY the exact name of the agent you select (e.g. 'Planner Agent'). Do not include any other text, reasoning, or markdown. If the task doesn't clearly match, select the 'General Chat Agent' as a fallback."""

        response = self.llm.execute(prompt=task, system=system_prompt)
        selected_agent_name = response.strip().replace("'", "").replace('"', '')
        
        if selected_agent_name not in self.registered_agents:
            logger.warning(f"LLM returned invalid agent name '{selected_agent_name}'. Falling back to General Chat Agent.")
            selected_agent_name = "General Chat Agent"
            
        logger.info(f"Task dynamically routed to {selected_agent_name}")
        return self.registered_agents[selected_agent_name]

    def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Processes the task by routing it to the appropriate specialized agent.
        """
        logger.info(f"RouterAgent received task: {task}")
        try:
            target_agent = self.route(task)
            return target_agent.process_task(task, context)
        except Exception as e:
            logger.error(f"Error during task routing: {e}")
            raise

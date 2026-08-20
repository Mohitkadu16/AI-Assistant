# pyrefly: ignore [missing-import]
from src.configs.settings import settings
# pyrefly: ignore [missing-import]
from src.utils.logger import logger
# pyrefly: ignore [missing-import]
from src.agents.router_agent import RouterAgent
# pyrefly: ignore [missing-import]
from src.agents.base_agent import BaseAgent
from typing import Any, Dict, Optional
import sys

from src.agents.planner_agent import PlannerAgent
from src.agents.research_agent import ResearchAgent
from src.agents.social_media_agent import SocialMediaAgent
from src.agents.coding_agent import CodingAgent
from src.agents.electronics_pcb_agent import ElectronicsPCBAgent
from src.agents.video_editing_agent import VideoEditingAgent
from src.agents.photography_agent import PhotographyAgent
from src.agents.studkits_business_agent import StudKitsBusinessAgent
from src.agents.project_manager_agent import ProjectManagerAgent
from src.agents.memory_agent import MemoryAgent

def main() -> None:
    logger.info("Initializing Personal AI Workspace...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Workspace Directory: {settings.workspace_dir}")

    # Initialize Master Router Agent
    router = RouterAgent()

    # Initialize and register specialized agents
    router.register_agent(PlannerAgent())
    router.register_agent(ResearchAgent())
    router.register_agent(SocialMediaAgent())
    router.register_agent(CodingAgent())
    router.register_agent(ElectronicsPCBAgent())
    router.register_agent(VideoEditingAgent())
    router.register_agent(PhotographyAgent())
    router.register_agent(StudKitsBusinessAgent())
    router.register_agent(ProjectManagerAgent())
    router.register_agent(MemoryAgent())

    # Interactive REPL loop
    print("\n=== Personal AI Workspace ===")
    print("Type 'exit' or 'quit' to close.")
    
    while True:
        try:
            if len(sys.argv) > 1 and len(sys.argv) != 0:
                user_task = " ".join(sys.argv[1:])
                sys.argv = [sys.argv[0]] # clear args so it doesn't loop infinitely
            else:
                user_task = input("\nEnter your task: ")
                
            if not user_task.strip():
                continue
                
            if user_task.strip().lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            logger.info(f"User Request: {user_task}")
            
            result = router.process_task(user_task)
            logger.info(f"Task execution result: {result}")
            print(f"\nResult: {result}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Failed to execute task: {e}")
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

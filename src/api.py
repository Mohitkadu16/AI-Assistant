from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uuid
import os
import base64
from typing import Optional, List
from src.agents.router_agent import RouterAgent
from src.configs.settings import settings
from src.utils.chat_manager import ChatManager
from src.utils.file_parser import parse_file
import uvicorn

app = FastAPI(
    title="Personal AI Workspace API",
    description="API for routing tasks to specialized agents.",
    version="1.0.0"
)

# Mount static files for the Web UI
app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_DIR = os.path.join(settings.workspace_dir, "data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = RouterAgent()

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
from src.agents.chat_agent import ChatAgent

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
router.register_agent(ChatAgent())

class TaskRequest(BaseModel):
    task: str
    context: dict = {}
    session_id: Optional[str] = None
    target_agent: Optional[str] = "Auto"
    images: List[str] = [] # list of base64 strings
    file_contents: List[dict] = [] # list of {"filename": str, "content": str}

class TaskResponse(BaseModel):
    status: str
    result: dict
    session_id: str

@app.post("/api/v1/task", response_model=TaskResponse)
async def process_task(request: TaskRequest):
    try:
        if not request.task.strip():
            raise HTTPException(status_code=400, detail="Task cannot be empty.")
            
        session_id = request.session_id or str(uuid.uuid4())
        
        # Inject history into context
        history = ChatManager.get_session_history(session_id)
        request.context["history"] = history
        
        # Pass images to context for llm_tools to use
        if request.images:
            request.context["images"] = request.images
            
        # Append parsed file contents to the task prompt
        full_task = request.task
        if request.file_contents:
            file_texts = "\n\n".join([f"--- Attached File: {f['filename']} ---\n{f['content']}" for f in request.file_contents if f['content']])
            full_task = f"{file_texts}\n\nUser Request: {full_task}"
            
        # Routing logic
        if request.target_agent and request.target_agent != "Auto":
            if request.target_agent in router.registered_agents:
                target_agent_obj = router.registered_agents[request.target_agent]
                result = target_agent_obj.process_task(full_task, request.context)
            else:
                # fallback
                target_agent_obj = router.registered_agents.get("General Chat Agent", list(router.registered_agents.values())[0])
                result = target_agent_obj.process_task(full_task, request.context)
        else:
            result = router.process_task(full_task, request.context)
        
        # Extract agent name and response
        agent_name = result.get("agent", "Unknown Agent")
        agent_response = result.get("result", "")
        
        # Save turn
        ChatManager.save_turn(session_id, request.task, agent_name, agent_response)
        
        return TaskResponse(status="success", result={"agent_output": result}, session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    results = {"images": [], "file_contents": []}
    
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
            
        _, ext = os.path.splitext(file.filename)
        ext = ext.lower()
        
        if ext in ['.png', '.jpg', '.jpeg', '.webp']:
            # Convert to base64
            with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                results["images"].append(encoded_string)
        else:
            # Parse text/pdf
            content = parse_file(file_path)
            if content:
                results["file_contents"].append({"filename": file.filename, "content": content})
                
    return results

@app.get("/health")
async def health_check():
    return {"status": "ok", "environment": settings.environment}

@app.get("/api/v1/chats")
async def get_chats():
    return ChatManager.get_all_sessions()

@app.get("/api/v1/chats/{session_id}")
async def get_chat_history(session_id: str):
    history = ChatManager.get_session_history(session_id)
    if not history:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id, "history": history}

@app.get("/")
async def root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)

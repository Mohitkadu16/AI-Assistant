from typing import Any, List, Dict
from src.memory.base_memory import BaseMemory

class DocumentStore(BaseMemory):
    """
    Stub for a document store that handles MD, PDF, TXT, JSON.
    """
    
    def __init__(self):
        self.documents = {}
        
    def store(self, key: str, value: Any, metadata: Dict[str, Any] = None) -> None:
        # Stub implementation
        self.documents[key] = {"content": value, "metadata": metadata or {}}
        
    def retrieve(self, query: str) -> List[Any]:
        # Stub implementation
        return [f"Stub: Retrieved document matching '{query}'"]

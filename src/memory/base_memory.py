from abc import ABC, abstractmethod
from typing import Any, List, Dict

class BaseMemory(ABC):
    """
    Abstract Base Class for Memory storage and retrieval.
    """
    
    @abstractmethod
    def store(self, key: str, value: Any, metadata: Dict[str, Any] = None) -> None:
        """Store information in memory."""
        pass
        
    @abstractmethod
    def retrieve(self, query: str) -> List[Any]:
        """Retrieve information from memory based on a query."""
        pass

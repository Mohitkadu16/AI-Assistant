from typing import Any
from src.tools.base_tool import BaseTool

class FileSystemTool(BaseTool):
    def __init__(self):
        super().__init__(name="File System", description="Reads and writes local files.")

    def execute(self, action: str, path: str, content: str = None, **kwargs) -> Any:
        # Stub implementation
        return f"Stub: Performed {action} on {path}"

class PDFReaderTool(BaseTool):
    def __init__(self):
        super().__init__(name="PDF Reader", description="Extracts text from PDF files.")

    def execute(self, path: str, **kwargs) -> Any:
        # Stub implementation
        return f"Stub: Read PDF {path}"

class MarkdownReaderTool(BaseTool):
    def __init__(self):
        super().__init__(name="Markdown Reader", description="Parses markdown files.")

    def execute(self, path: str, **kwargs) -> Any:
        # Stub implementation
        return f"Stub: Read Markdown {path}"

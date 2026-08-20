from typing import Any
import requests
from src.tools.base_tool import BaseTool
from src.configs.settings import settings

class GeminiTool(BaseTool):
    def __init__(self):
        super().__init__(name="Gemini API", description="Accesses the Gemini model for generation.")

    def execute(self, prompt: str, **kwargs) -> Any:
        try:
            if not settings.gemini_api_key:
                return "Error: GEMINI_API_KEY is missing."
            from google import genai
            client = genai.Client(api_key=settings.gemini_api_key)
            
            # Use gemini-2.5-flash as default, unless specified
            model_name = kwargs.get('model', 'gemini-2.5-flash')
            
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            return f"Error calling Gemini API: {str(e)}"

class OllamaTool(BaseTool):
    def __init__(self, model_name: str = "qwen3"):
        super().__init__(name="Ollama API", description=f"Accesses local Ollama model: {model_name}")
        self.model_name = model_name

    def execute(self, prompt: str, **kwargs) -> Any:
        try:
            url = f"{settings.ollama_base_url}/api/generate"
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
            if "system" in kwargs:
                payload["system"] = kwargs["system"]
            if "images" in kwargs and kwargs["images"]:
                payload["images"] = kwargs["images"]
                
            response = requests.post(url, json=payload, timeout=300)
            if not response.ok:
                try:
                    error_msg = response.json().get("error", response.text)
                    return f"Ollama Error: {error_msg}. (Did you run 'ollama run {self.model_name}'?)"
                except:
                    response.raise_for_status()
            return response.json().get("response", "")
        except requests.exceptions.ConnectionError:
            return f"Error: Could not connect to Ollama at {settings.ollama_base_url}. Is Ollama running?"
        except Exception as e:
            return f"Error calling Ollama API: {str(e)}"

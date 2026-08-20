from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables and .env file.
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # API Keys
    gemini_api_key: str = Field(default="", description="Google Gemini API Key")
    ollama_base_url: str = Field(default="http://localhost:11434", description="Base URL for local Ollama instance")

    # App Config
    log_level: str = Field(default="INFO", description="Logging level (e.g., DEBUG, INFO, WARNING, ERROR)")
    environment: str = Field(default="development", description="Environment mode (development, production)")
    workspace_dir: str = Field(default="./workspace_data", description="Directory to store workspace data")

settings = Settings()

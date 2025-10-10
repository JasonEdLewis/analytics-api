from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
  """Application settings loaded from environment variables."""
  #API Configuration
  API_V1_PREFIX: str
  DEBUG: bool = False

  # DATABASE Config
  DATABASE_URL:str
  DATABASE_POOL_SIZE:int = 5
  DATABASE_MAX_OVERFLOW:int = 30
  # Security
  SECRET_KEY: str
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
  ALGORITHM: str = "HS256"

  # CORS
  BACKEND_CORS_ORIGINS: List[str] = []
  
  model_config = SettingsConfigDict(
    env_file=".env",
    case_sensitive=True,
    extra="ignore"
  )

settings = Settings()
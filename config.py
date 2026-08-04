from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
  
    APP_NAME: str = "Enterprise AI Knowledge Assistant"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    ALGORITHM: str = "HS256"


    DATABASE_URL: str = "sqlite:///./enterprise_ai.db"

    
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

   
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

   
    FAISS_INDEX_PATH: str = "./data/faiss_index"
    UPLOAD_DIR: str = "./data/uploads"

   
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K: int = 5
    TEMPERATURE: float = 0.3
    MAX_TOKENS: int = 2048

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    ALLOW_ORIGINS: str = '*'
    openai_api_key: str
    MODEL: str = 'gpt-4o-2024-08-06'
    EMBEDDING_MODEL: str = 'text-embedding-3-large'
    EMBEDDING_DIMENSIONS: int = 1024
    model_config = SettingsConfigDict(env_file='./.env')
    
settings = Settings()

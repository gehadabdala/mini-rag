from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  
        App_Name: str
        App_Version: str
        OpenAI_API_Key: str
        FILE_ALLOWED_TYPES: list
        MAX_FILE_SIZE_MB: int
        FILE_DEFAULT_CHUNK_SIZE: int
        class Config:
            env_file = ".env"


def get_settings():
    return Settings()


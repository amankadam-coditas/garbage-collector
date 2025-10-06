from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL : str
    SECRET : str 
    ALGORITHM : str = "HS256"
    
    class Config():
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

setting = Settings()
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL : str
    SECRET : str 
    ALGORITHM : str = "HS256"
    JWT_ALGORITHM : str = "HS256" 
    ACCESS_TOKEN_EXPIRTY_TIMEOUT : int = 15
    
    class Config():
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

setting = Settings()
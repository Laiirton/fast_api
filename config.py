import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class Settings(BaseSettings):
    # Configurações do Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
    SUPABASE_JWT_SECRET: str = os.getenv("SUPABASE_JWT_SECRET")
    
    # Configurações de JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "3600"))
    
    # Configurações de CORS
    CORS_ORIGINS: list = [
        "exp://192.168.0.4:8081",
        "http://localhost:8081",
        "http://localhost:8000",
        "http://localhost:3000",
        "https://*.vercel.app",
    ]
    
    # Configurações da API
    API_PREFIX: str = "/api"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instância das configurações
settings = Settings()

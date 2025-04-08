from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routes import auth, users

# Cria a aplicação FastAPI
app = FastAPI(
    title="API Serviços Urbanos",
    description="API para gerenciamento de usuários",
    version="1.0.0"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(users.router, prefix=settings.API_PREFIX)

@app.get("/")
async def root():
    """
    Rota raiz da API
    """
    return {
        "message": "API de Usuários",
        "version": "1.0.0",
        "status": "online"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

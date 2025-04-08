from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from database import get_supabase_client
from models.user import UserCreate, UserLogin, Token
from utils.auth import get_password_hash, verify_password, create_access_token
from config import settings

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/register", response_model=Token)
async def register_user(user_data: UserCreate):
    """
    Registra um novo usuário no sistema
    """
    supabase = get_supabase_client()
    
    # Verifica se o usuário já existe
    existing_user = supabase.table("users").select("*").eq("username", user_data.username).execute()
    if existing_user.data and len(existing_user.data) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de usuário já está em uso"
        )
    
    # Verifica se o email já existe
    existing_email = supabase.table("users").select("*").eq("email", user_data.email).execute()
    if existing_email.data and len(existing_email.data) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está em uso"
        )
    
    # Verifica se o CPF já existe
    existing_cpf = supabase.table("users").select("*").eq("cpf", user_data.cpf).execute()
    if existing_cpf.data and len(existing_cpf.data) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já está em uso"
        )
    
    # Cria o hash da senha
    hashed_password = get_password_hash(user_data.password)
    
    # Prepara os dados para inserção
    user_dict = user_data.model_dump()
    user_dict["password"] = hashed_password
    user_dict["status"] = "active"  # Status padrão
    user_dict["role"] = "user"      # Papel padrão
    
    # Insere o usuário no banco de dados
    result = supabase.table("users").insert(user_dict).execute()
    
    if not result.data or len(result.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar usuário"
        )
    
    # Cria o token de acesso
    user_id = result.data[0]["id"]
    access_token = create_access_token(
        data={"sub": user_data.username, "id": user_id},
        expires_delta=timedelta(seconds=settings.JWT_ACCESS_TOKEN_EXPIRES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Autentica um usuário e retorna um token de acesso
    """
    supabase = get_supabase_client()
    
    # Busca o usuário pelo nome de usuário
    user_result = supabase.table("users").select("*").eq("username", form_data.username).execute()
    
    if not user_result.data or len(user_result.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = user_result.data[0]
    
    # Verifica se a senha está correta
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Atualiza o último login
    supabase.table("users").update({"last_login": "now()"}).eq("id", user["id"]).execute()
    
    # Cria o token de acesso
    access_token = create_access_token(
        data={"sub": user["username"], "id": user["id"]},
        expires_delta=timedelta(seconds=settings.JWT_ACCESS_TOKEN_EXPIRES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from database import get_supabase_client
from models.user import UserResponse
from utils.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Usuários"])

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Retorna as informações do usuário autenticado
    """
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna as informações de um usuário específico pelo ID (apenas o próprio usuário ou um administrador pode acessar)
    """
    # Verifica se o usuário atual tem permissão para acessar esses dados
    # (apenas o próprio usuário ou um administrador pode acessar)
    if current_user["id"] != user_id and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para acessar esses dados"
        )
    
    supabase = get_supabase_client()
    user_result = supabase.table("users").select("*").eq("id", user_id).execute()
    
    if not user_result.data or len(user_result.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return user_result.data[0]

@router.get("/", response_model=List[UserResponse])
async def get_all_users(current_user: dict = Depends(get_current_user)):
    """
    Retorna a lista de todos os usuários (apenas para administradores)
    """
    # Verifica se o usuário atual é um administrador
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem acessar essa rota"
        )
    
    supabase = get_supabase_client()
    users_result = supabase.table("users").select("*").execute()
    
    return users_result.data

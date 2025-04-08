from supabase import create_client
from config import settings

# Cria o cliente do Supabase
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def get_supabase_client():
    """
    Retorna o cliente do Supabase para uso nas rotas
    """
    return supabase

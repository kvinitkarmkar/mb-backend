from supabase import create_client, Client
from app.core.config import settings

supabase: Client = None


def init_supabase():
    global supabase
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    print("âœ… Supabase connected")


def get_supabase() -> Client:
    return supabase

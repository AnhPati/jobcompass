import os
import streamlit as st

def is_render_environment():
    """Détecte si on est sur Render"""
    return os.environ.get("RENDER") is not None or "onrender.com" in os.environ.get("RENDER_EXTERNAL_URL", "")

def get_config(key: str, default: str = None):
    """
    Récupère une config depuis les variables d'environnement (Render) 
    ou depuis st.secrets (local).
    """
    # Essaie d'abord les variables d'environnement (Render)
    value = os.environ.get(key)
    if value:
        return value
    
    # Sinon essaie st.secrets (local)
    try:
        return st.secrets[key]
    except (KeyError, AttributeError):
        return default

# Variables globales pour l'app
SUPABASE_URL = get_config("SUPABASE_URL")
SUPABASE_KEY = get_config("SUPABASE_KEY") 
SUPABASE_BUCKET = get_config("SUPABASE_BUCKET", "users-markets")
def get_testing_mode():
    value = get_config("testing_mode", False)
    if isinstance(value, bool):
        return value
    return str(value).lower() == "true"

TESTING_MODE = get_testing_mode()
IS_RENDER = is_render_environment()
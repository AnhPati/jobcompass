import streamlit as st
from components.auth.native_auth import native_login_form
from menu import unauthenticated_menu

def login_form():
    """Point d'entrée de connexion - utilise l'auth native Streamlit"""
    
    # Tentative de connexion avec l'auth native
    authenticated = native_login_form()
    
    if authenticated:
        # Utilisateur connecté - redirection vers l'app
        st.success("✅ Connexion réussie !")
        st.switch_page("pages/App.py")
    else:
        # Menu non authentifié si pas de session
        unauthenticated_menu()
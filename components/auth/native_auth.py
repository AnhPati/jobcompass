import streamlit as st

def native_login_form():
    """Formulaire de connexion avec l'authentification native Streamlit"""
    
    # Vérification temporaire - st.user pas encore disponible
    if not hasattr(st, 'user') or not st.user.is_logged_in:
        # Interface de connexion
        st.title("🧭 JobCompass - Connexion")
        
        # Logo
        logo = "public/streamlit-logo.svg"
        left_co, cent_co, last_co = st.columns(3)
        with cent_co:
            try:
                st.image(logo)
            except:
                st.write("🧭 **JobCompass**")
        
        st.markdown("### 🔐 Connectez-vous pour accéder à JobCompass")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.button(
                "🐱 Continuer avec GitHub", 
                on_click=st.login, 
                args=["github"],
                use_container_width=True
            )
            
        with col2:
            st.button(
                "🔍 Continuer avec Google", 
                on_click=st.login, 
                args=["google"],
                use_container_width=True
            )
        
        # Arrêter l'exécution si pas connecté
        st.stop()
    
    else:
        # Utilisateur connecté - configuration de la session JobCompass
        setup_user_session()
        return True

def setup_user_session():
    """Configure la session JobCompass avec les données utilisateur"""
    
    # Récupération des infos utilisateur depuis st.user
    user_info = {
        "id": st.user.get("sub"),  # Subject = ID utilisateur unique
        "email": st.user.get("email"),
        "name": st.user.get("name"),
        "picture": st.user.get("picture"),
        "provider": st.user.get("iss", "unknown")  # Issuer = provider
    }
    
    # Migration vers le format de session JobCompass existant
    st.session_state['user'] = user_info
    st.session_state['access_token'] = st.user.get("sub")  # Utiliser l'ID comme token
    st.session_state.role = "user"

def logout():
    """Déconnexion complète"""
    # Nettoyer les données JobCompass
    for key in ['user', 'access_token', 'role']:
        if key in st.session_state:
            del st.session_state[key]
    
    # Déconnexion native Streamlit
    st.logout()

def is_user_authenticated():
    """Vérifie si l'utilisateur est connecté"""
    return st.user.is_logged_in

def get_user_id():
    """Récupère l'ID unique de l'utilisateur connecté"""
    if st.user.is_logged_in:
        return st.user.get("sub")
    return None
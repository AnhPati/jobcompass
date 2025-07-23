import streamlit as st
from streamlit_supabase_auth import login_form as supabase_login_form, logout_button
from menu import unauthenticated_menu

from utils.config import SUPABASE_URL, SUPABASE_KEY

def login_form():
    st.title("Streamlit SaaS Starter Login Page")

    logo = "public/streamlit-logo.svg"
    left_co, cent_co, last_co = st.columns(3)
    with cent_co:
        st.image(logo)

    # ✅ Utilisation du composant original du template
    session = supabase_login_form(
        url=SUPABASE_URL,
        apiKey=SUPABASE_KEY,
        providers=["github", "google"]
    )

    # Debug: Vérifier les paramètres URL pour le callback OAuth
    query_params = st.query_params
    if query_params:
        st.info(f"🔍 Debug - Paramètres URL: {dict(query_params)}")
    
    # Debug: Afficher l'état de la session
    if session:
        st.success(f"🔍 Debug - Session trouvée: {type(session)}")
    else:
        st.warning("🔍 Debug - Aucune session détectée")

    if session:
        # 🔐 Gestion de session selon le template original
        user = session.get("user", {})
        jwt = (
            session.get("access_token") or
            session.get("accessToken") or
            session.get("idToken")
        )
        
        # Injection du token pour cohérence avec helpers.py
        user["jwt"] = jwt
        user["access_token"] = jwt

        st.session_state['user'] = user
        st.session_state['access_token'] = jwt
        st.session_state.role = "user"

        st.success("✅ Connexion réussie !")
        st.switch_page("pages/App.py")

        # Sidebar avec logout
        with st.sidebar:
            st.markdown(f"**Logged in as: *{user.get('email', 'unknown')}***")
            if logout_button(url=SUPABASE_URL, apiKey=SUPABASE_KEY):
                st.rerun()
    else:
        # Menu non authentifié si pas de session
        unauthenticated_menu()
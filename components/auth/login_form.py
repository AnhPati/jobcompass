import streamlit as st
from st_supabase_connection import SupabaseConnection
from supabase import create_client, Client
from menu import menu, unauthenticated_menu

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Clients Supabase selon usage
conn = st.connection("supabase", type=SupabaseConnection)  # Pour DB
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)  # Pour OAuth

def login_form():
    st.title("Streamlit SaaS Starter Login Page")

    # ✅ DEBUG: Voir l'URL actuelle et les query params
    st.write(f"🔍 **URL actuelle**: {st.get_option('browser.serverAddress')}")
    st.write(f"🔍 **Query params**: {dict(st.query_params)}")
    st.write(f"🔍 **Session state keys**: {list(st.session_state.keys())}")

    logo = "public/streamlit-logo.svg"
    left_co, cent_co, last_co = st.columns(3)
    with cent_co:
        st.image(logo)

    # ✅ Vérifier session existante d'abord
    if 'user' in st.session_state and st.session_state.get('access_token'):
        st.success(f"Connecté : {st.session_state.user.get('email')}")
        if st.button("Accéder à l'app"):
            st.switch_page("pages/App.py")
        if st.button("Se déconnecter"):
            for key in ['user', 'access_token', 'role']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        return
    
    # ✅ Interface OAuth manuelle avec boutons
    st.markdown("### Se connecter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🐙 GitHub", use_container_width=True, type="primary"):
            try:
                response = supabase.auth.sign_in_with_oauth({
                    "provider": "github"
                })
                if response.url:
                    st.markdown(f'<meta http-equiv="refresh" content="0; url={response.url}">', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erreur GitHub : {e}")
    
    with col2:
        if st.button("🌐 Google", use_container_width=True, type="secondary"):
            try:
                response = supabase.auth.sign_in_with_oauth({
                    "provider": "google"
                })
                if response.url:
                    st.markdown(f'<meta http-equiv="refresh" content="0; url={response.url}">', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erreur Google : {e}")
    
    # ✅ Traitement callback OAuth
    params = dict(st.query_params)
    access_token = params.get('access_token')
    refresh_token = params.get('refresh_token')
    
    session = None
    if access_token:
        try:
            if refresh_token:
                supabase.auth.set_session(access_token, refresh_token)
            
            user_response = supabase.auth.get_user(access_token)
            
            if user_response.user:
                session = {
                    'user': {
                        'id': user_response.user.id,
                        'email': user_response.user.email,
                        'user_metadata': user_response.user.user_metadata or {},
                    },
                    'access_token': access_token,
                    'accessToken': access_token,
                    'idToken': access_token
                }
                # Nettoyer les query params
                st.query_params.clear()
        except Exception as e:
            st.error(f"❌ Erreur callback : {e}")

    # ✅ DEBUG: Voir ce que retourne le traitement OAuth
    if session:
        st.write(f"🔍 **Session object**: {session}")
        st.write(f"🔍 **Session type**: {type(session)}")

    if session:
        st.write(f"🔍 **Session keys**: {list(session.keys()) if hasattr(session, 'keys') else 'Not a dict'}")

        # 🔐 Extraction robuste du token
        jwt = (
            session.get("access_token") or
            session.get("accessToken") or
            session.get("idToken")
        )

        user = session.get("user", {})
        user["jwt"] = jwt  # Injection explicite

        st.session_state['user'] = user
        st.session_state['access_token'] = jwt
        st.session_state.role = "user"

        st.success("✅ Connexion réussie !")
        st.switch_page("pages/App.py")

        with st.sidebar:
            st.markdown(f"**Logged in as: *{user.get('email', 'unknown')}***")
            if st.button("Se déconnecter", key="sidebar_logout"):
                for key in ['user', 'access_token', 'role']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
    # Menu non authentifié seulement si pas de session
    if 'user' not in st.session_state:
        unauthenticated_menu()
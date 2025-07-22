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
    with st.expander("🔍 Debug Info (dev only)", expanded=False):
        st.write(f"**Query params**: {dict(st.query_params)}")
        st.write(f"**Session state keys**: {list(st.session_state.keys())}")
        try:
            st.write(f"**URL actuelle**: {st.get_option('browser.serverAddress')}")
        except:
            st.write("**URL actuelle**: Non disponible")

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
    
    # ✅ Interface OAuth avec liens directs (compatible Streamlit Cloud)
    st.markdown("### Se connecter")
    
    # URLs OAuth directes de Supabase
    github_url = f"{SUPABASE_URL}/auth/v1/authorize?provider=github&redirect_to=https://jobcompass.streamlit.app"
    google_url = f"{SUPABASE_URL}/auth/v1/authorize?provider=google&redirect_to=https://jobcompass.streamlit.app"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <a href="{github_url}" target="_self" style="
            display: inline-block;
            width: 100%;
            padding: 0.75rem 1rem;
            background-color: #24292e;
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 0.375rem;
            font-weight: 500;
            font-size: 1rem;
            transition: background-color 0.2s;
            margin-bottom: 0.5rem;
        " onmouseover="this.style.backgroundColor='#1a1e22'" onmouseout="this.style.backgroundColor='#24292e'">
            🐙 Se connecter avec GitHub
        </a>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <a href="{google_url}" target="_self" style="
            display: inline-block;
            width: 100%;
            padding: 0.75rem 1rem;
            background-color: #4285f4;
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 0.375rem;
            font-weight: 500;
            font-size: 1rem;
            transition: background-color 0.2s;
            margin-bottom: 0.5rem;
        " onmouseover="this.style.backgroundColor='#3367d6'" onmouseout="this.style.backgroundColor='#4285f4'">
            🌐 Se connecter avec Google
        </a>
        """, unsafe_allow_html=True)
    
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
        with st.expander("🔍 Session Debug (dev only)", expanded=False):
            st.write(f"**Session object**: {session}")
            st.write(f"**Session type**: {type(session)}")

    if session:
        with st.expander("🔍 Session Details (dev only)", expanded=False):
            st.write(f"**Session keys**: {list(session.keys()) if hasattr(session, 'keys') else 'Not a dict'}")
            st.write(f"**User data**: {session.get('user', {})}")

        # 🔐 Extraction robuste du token
        jwt = (
            session.get("access_token") or
            session.get("accessToken") or
            session.get("idToken")
        )

        user = session.get("user", {})
        user["jwt"] = jwt  # Injection explicite
        user["access_token"] = jwt  # Cohérence avec helpers.py

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
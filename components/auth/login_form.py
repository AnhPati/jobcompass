import streamlit as st
from st_supabase_connection import SupabaseConnection
from supabase import create_client, Client
from menu import unauthenticated_menu

def login_form():
    st.title("Streamlit SaaS Starter Login Page")

    logo = "public/streamlit-logo.svg"
    left_co, cent_co, last_co = st.columns(3)
    with cent_co:
        st.image(logo)

    # ✅ Vérifier session existante
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

    # ✅ SOLUTION CORRECTE : Deux clients selon l'usage
    try:
        # Pour les requêtes DB (avec cache)
        conn = st.connection("supabase", type=SupabaseConnection)
        
        # Pour l'OAuth (client Supabase natif - sans cache)
        SUPABASE_URL = st.secrets["SUPABASE_URL"] 
        SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
        oauth_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
    except Exception as e:
        st.error(f"Erreur connexion Supabase : {e}")
        return

    # ✅ Interface OAuth avec client natif
    st.markdown("### Se connecter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🐙 GitHub", use_container_width=True, type="primary"):
            try:
                # ✅ CORRECT : OAuth avec client natif
                response = oauth_client.auth.sign_in_with_oauth({
                    "provider": "github",
                    "options": {
                        "redirect_to": "https://jobcompass.streamlit.app"
                    }
                })
                if response.url:
                    st.markdown(f'<meta http-equiv="refresh" content="0; url={response.url}">', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erreur GitHub : {e}")
    
    with col2:
        if st.button("🌐 Google", use_container_width=True, type="secondary"):
            try:
                # ✅ CORRECT : OAuth avec client natif
                response = oauth_client.auth.sign_in_with_oauth({
                    "provider": "google",
                    "options": {
                        "redirect_to": "https://jobcompass.streamlit.app"
                    }
                })
                if response.url:
                    st.markdown(f'<meta http-equiv="refresh" content="0; url={response.url}">', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erreur Google : {e}")

    # ✅ Traitement callback avec client natif 
    params = dict(st.query_params)
    access_token = params.get('access_token')
    refresh_token = params.get('refresh_token')
    
    if access_token:
        try:
            # Session avec client natif
            if refresh_token:
                oauth_client.auth.set_session(access_token, refresh_token)
            
            user_response = oauth_client.auth.get_user(access_token)
            
            if user_response.user:
                # Session state comme avant
                st.session_state['user'] = {
                    'id': user_response.user.id,
                    'email': user_response.user.email,
                    'user_metadata': user_response.user.user_metadata,
                    'jwt': access_token
                }
                st.session_state['access_token'] = access_token
                st.session_state['role'] = "user"
                
                # Nettoyer et rediriger
                st.query_params.clear()
                st.success("✅ Connexion réussie !")
                st.switch_page("pages/App.py")
            else:
                st.error("❌ Erreur utilisateur")
        except Exception as e:
            st.error(f"❌ Erreur callback : {e}")

    # Menu non authentifié
    if 'user' not in st.session_state:
        unauthenticated_menu()

# ✅ EXPLICATION :
# - st-supabase-connection : Pour les requêtes DB avec cache
# - Client Supabase natif : Pour l'OAuth (non supporté par le connector)
# - Même result que streamlit-supabase-auth mais compatible Streamlit Cloud
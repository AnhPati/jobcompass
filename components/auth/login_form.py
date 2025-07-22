# ✅ SOLUTION MINIMALE : Remplacer juste la partie authentification

# Dans requirements.txt, remplacez :
# streamlit-supabase-auth  ❌
# Par :
# st-supabase-connection   ✅

# Dans login_form.py, remplacez la fonction login_form par :
import streamlit as st
from st_supabase_connection import SupabaseConnection
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

    # ✅ Connexion moderne avec st-supabase-connection
    try:
        conn = st.connection("supabase", type=SupabaseConnection)
        supabase = conn._client
    except Exception as e:
        st.error(f"Erreur connexion Supabase : {e}")
        return

    # ✅ Interface OAuth propre
    st.markdown("### Se connecter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🐙 GitHub", use_container_width=True, type="primary"):
            # URL OAuth directe
            auth_url = f"{st.secrets['SUPABASE_URL']}/auth/v1/authorize?provider=github&redirect_to=https://jobcompass.streamlit.app"
            st.markdown(f'<meta http-equiv="refresh" content="0; url={auth_url}">', unsafe_allow_html=True)
    
    with col2:
        if st.button("🌐 Google", use_container_width=True, type="secondary"):
            # URL OAuth directe  
            auth_url = f"{st.secrets['SUPABASE_URL']}/auth/v1/authorize?provider=google&redirect_to=https://jobcompass.streamlit.app"
            st.markdown(f'<meta http-equiv="refresh" content="0; url={auth_url}">', unsafe_allow_html=True)

    # ✅ Traitement callback
    params = dict(st.query_params)
    access_token = params.get('access_token')
    refresh_token = params.get('refresh_token')
    
    if access_token:
        try:
            # Session avec tokens
            supabase.auth.set_session(access_token, refresh_token or "")
            user_response = supabase.auth.get_user()
            
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
                
                # Nettoyer URL et rediriger
                st.query_params.clear()
                st.success("✅ Connexion réussie !")
                st.switch_page("pages/App.py")
            else:
                st.error("❌ Erreur utilisateur")
        except Exception as e:
            st.error(f"❌ Erreur auth : {e}")
    
    # Menu non authentifié
    if 'user' not in st.session_state:
        unauthenticated_menu()

# ✅ Le reste de votre template reste IDENTIQUE
# - Toute la logique métier
# - La structure des pages  
# - Les composants UI
# - La config Stripe
# - etc.

# Seule la partie authentification change !
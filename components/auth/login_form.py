import streamlit as st
from streamlit_supabase_auth import login_form as supabase_login_form, logout_button
from supabase import create_client, Client
from menu import menu, unauthenticated_menu

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

    session = supabase_login_form(
        url=SUPABASE_URL,
        apiKey=SUPABASE_KEY,
        providers=["github", "google"]
    )

    # ✅ DEBUG: Voir ce que retourne supabase_login_form
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
        st.session_state['access_token'] = jwt  # optionnel, mais pratique
        st.session_state.role = "user"

        st.query_params.login = ["success"]
        st.switch_page("pages/App.py")

        with st.sidebar:
            st.markdown(f"**Logged in as: *{user.get('email', 'unknown')}***")
            if logout_button(url=SUPABASE_URL, apiKey=SUPABASE_KEY):
                print("Logging out.")
    else:
        st.write("❌ **Aucune session détectée**")
        unauthenticated_menu()
import streamlit as st
# Import config pour Render avant tout
try:
    import config_render
except:
    pass

from utils.helpers import initialize_session_state, is_user_authenticated

st.set_page_config(page_title="JobCompass", page_icon="🧭", layout="wide")

# Initialise l'état de la session au tout début
initialize_session_state()

def main():
    # Vérifie l'état d'authentification de l'utilisateur
    if is_user_authenticated():
        st.switch_page("pages/App.py")
    else:
        st.switch_page("pages/Login.py")

if __name__ == "__main__":
    main()
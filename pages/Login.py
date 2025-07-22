import streamlit as st

st.set_page_config(
    page_title="Authentification",
    page_icon="🌍",
    layout="centered"
)
st.set_option("client.showSidebarNavigation", False)

# Imports après set_page_config pour éviter l'exécution de commandes Streamlit
from components.auth.login_form import login_form
from utils.helpers import is_user_authenticated

# Si l'utilisateur est déjà connecté, le rediriger vers l'application
if is_user_authenticated():
    st.switch_page("pages/App.py")

login_form()

st.page_link("pages/Landing.py", label="Retour à l'accueil", icon="🏠")
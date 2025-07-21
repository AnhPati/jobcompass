import streamlit as st
from utils.helpers import is_user_authenticated

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/Landing.py", label="Accueil")
    st.sidebar.page_link("pages/App.py", label="JobCompass")
    st.sidebar.page_link("pages/Login.py", label="Logout")

    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.page_link("pages/admin.py", label="Manage users")
        st.sidebar.page_link(
            "pages/super-admin.py",
            label="Manage admin access",
            disabled=st.session_state.role != "super-admin",
        )

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("pages/Landing.py", label="Accueil")
    st.sidebar.page_link("pages/Login.py", label="Login")

def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if not is_user_authenticated():
        unauthenticated_menu()
        return
    authenticated_menu()

def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if 'user' not in st.session_state or st.session_state.role is None:
        st.switch_page("pages/Login.py")
    print("role", st.session_state.role)
    menu()

def menu_home():
    menu()
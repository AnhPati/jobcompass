import streamlit as st
from constants.texts import APP_INTRO, APP_HOWTO, APP_HELP

def render_home():

    st.title("Bienvenue sur JobCompass")
    st.markdown("---")

    st.markdown(APP_INTRO)
    st.markdown(APP_HOWTO)
    st.markdown(APP_HELP)

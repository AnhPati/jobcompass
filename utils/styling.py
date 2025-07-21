import streamlit as st

def style_anchor(class_name: str):
    st.markdown(f'<div class="{class_name}"></div>', unsafe_allow_html=True)
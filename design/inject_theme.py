import streamlit as st
from pathlib import Path

def inject_theme():
    css_path = Path("design/theme.css")
    if css_path.exists():
        with css_path.open(encoding="utf-8") as f:  # ✅ Forcer l'encodage UTF-8
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("Le fichier design/theme.css est introuvable. Le thème n'a pas pu être appliqué.")
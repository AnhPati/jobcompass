import streamlit as st
import st_cookie
from config.settings import get_market_offers_remote_path

st.title("🔓 Déconnexion")

st.warning("📥 Avant de vous déconnecter, avez-vous bien téléchargé votre fichier CSV ?")

col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Non, revenir en arrière"):
        st.switch_page("app.py")  # ✅ fichier principal

with col2:
    if st.button("✅ Oui, je peux me déconnecter"):
        # 👇 Logique de déconnexion FAKE uniquement
        user_id = st.session_state.get("user", {}).get("id")
        if user_id:
            local_csv_path = get_market_offers_remote_path(user_id)
            if local_csv_path.exists():
                local_csv_path.unlink()

        for key in ["user_email", "user_id", "user_token"]:
            try:
                st_cookie.remove(key)
            except KeyError:
                pass

        st.session_state.clear()
        st.switch_page("app.py") 
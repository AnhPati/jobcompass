import streamlit as st

st.title("🧭 JobCompass - Test Deployment")
st.write("✅ If you can see this, Streamlit is working!")
st.write("🌍 Environment: Render.com")

# Test variables d'environnement
try:
    supabase_url = st.secrets.get("SUPABASE_URL", "Not found")
    st.write(f"🔧 Supabase URL: {supabase_url[:50]}...")
    st.success("✅ Secrets loaded successfully!")
except Exception as e:
    st.error(f"❌ Error loading secrets: {e}")

st.balloons()
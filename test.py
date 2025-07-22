import streamlit as st

st.title("🧭 JobCompass - Test Deployment")
st.write("✅ If you can see this, Streamlit is working!")
st.write("🌍 Environment: Render.com")

# Test variables d'environnement
try:
    # Streamlit sur Render utilise os.environ, pas st.secrets
    import os
    supabase_url = os.environ.get("SUPABASE_URL", "Not found")
    st.write(f"🔧 Supabase URL: {supabase_url[:50]}...")
    
    if supabase_url != "Not found":
        st.success("✅ Environment variables loaded successfully!")
    else:
        st.error("❌ SUPABASE_URL not found in environment")
        
except Exception as e:
    st.error(f"❌ Error loading environment: {e}")

st.balloons()
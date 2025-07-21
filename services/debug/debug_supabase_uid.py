import streamlit as st
import requests

def debug_supabase_auth():
    """
    Debug pour vérifier l'UUID réel de l'utilisateur dans Supabase
    """
    try:
        user = st.session_state.get("user")
        jwt = user.get("jwt") if user else None
        
        if not jwt:
            st.error("Pas de JWT trouvé")
            return
            
        # Headers d'authentification
        headers = {
            'Authorization': f'Bearer {jwt}',
            'apikey': st.secrets["SUPABASE_KEY"],
            'Content-Type': 'application/json'
        }
        
        # Appel à l'API Supabase pour récupérer l'utilisateur actuel
        user_url = f"{st.secrets['SUPABASE_URL']}/auth/v1/user"
        
        response = requests.get(user_url, headers=headers)
        
        if response.status_code == 200:
            auth_user = response.json()
            st.write("## 🔐 Utilisateur Supabase Auth :")
            st.json(auth_user)
            
            # Comparer avec votre session
            session_user_id = st.session_state.user.get("id")
            supabase_uid = auth_user.get("id")
            
            st.write("## 🆔 Comparaison des IDs :")
            st.write(f"**Votre session user ID**: `{session_user_id}`")
            st.write(f"**Supabase auth.uid()**: `{supabase_uid}`")
            
            if session_user_id == supabase_uid:
                st.success("✅ Les IDs correspondent !")
            else:
                st.error("❌ Les IDs ne correspondent pas ! C'est le problème.")
                
                # Suggestion de correction
                st.write("### 💡 Solutions possibles :")
                st.write("1. **Utiliser l'UUID Supabase** dans vos chemins")
                st.write("2. **Modifier les politiques RLS** pour accepter votre ID")
                
        else:
            st.error(f"Erreur API Auth : {response.status_code} - {response.text}")
            
    except Exception as e:
        st.error(f"Erreur debug auth : {str(e)}")

# À ajouter temporairement dans App.py
# debug_supabase_auth()
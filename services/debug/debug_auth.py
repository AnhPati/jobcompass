import streamlit as st
import json

def debug_auth():
    """
    Fonction de debug pour analyser votre structure d'authentification
    À ajouter temporairement dans App.py pour diagnostiquer
    """
    st.write("## 🔍 Debug Authentification")
    
    # Debug session_state complet
    st.write("### Session State Keys:")
    st.write(list(st.session_state.keys()))
    
    # Debug utilisateur
    user = st.session_state.get("user")
    if user:
        st.write("### Structure User:")
        st.json(user, expanded=False)
        
        st.write("### User Keys détaillées:")
        for key, value in user.items():
            st.write(f"**{key}**: {type(value)} - {str(value)[:100]}...")
            
        # Recherche spécifique de tokens
        st.write("### Tokens trouvés:")
        token_keys = ['access_token', 'accessToken', 'idToken', 'id_token', 
                     'token', 'authToken', 'jwt', 'bearer_token', 'refresh_token', 'refreshToken']
        
        tokens_found = {}
        for key in token_keys:
            if key in user and user[key]:
                tokens_found[key] = f"{str(user[key])[:20]}..."
        
        if tokens_found:
            st.json(tokens_found)
        else:
            st.error("Aucun token trouvé!")
    else:
        st.error("Pas d'utilisateur en session")
    
    # Debug autres clés de session possibles
    st.write("### Autres clés session_state liées à l'auth:")
    auth_keys = [k for k in st.session_state.keys() if 'auth' in k.lower() or 'token' in k.lower()]
    for key in auth_keys:
        st.write(f"**{key}**: {type(st.session_state[key])} - {str(st.session_state[key])[:100]}...")

# À ajouter temporairement dans App.py après st.title("JobCompass"):
# debug_auth()  # Décommentez cette ligne pour voir les infos de debug
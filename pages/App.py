import streamlit as st
from utils.helpers import is_user_authenticated
from tabs.home import render_home
from tabs.market_analysis import render_market_analysis
from tabs.offer_dissection import render_offer_dissection
from tabs.compass import render_compass
from components.csv_uploader import csv_uploader
from config.settings import get_market_offers_remote_path, get_market_offers_local_file
from services.cache.geocoding_cache import load_cache
from services.storage.market_file import ensure_market_file_exists
from design.inject_theme import inject_theme
from services.debug.debug_auth import debug_auth
from services.debug.debug_supabase_uid import debug_supabase_auth
import time

# ✅ Import du service de synchronisation
from services.sync.sync_service import (
    initialize_sync_state, 
    should_auto_sync, 
    sync_to_cloud, 
    get_sync_status_display,
    sync_on_disconnect
)

# 🔹 Config Streamlit & Garde de sécurité
st.set_page_config(page_title="JobCompass", layout="wide")
inject_theme()

if not is_user_authenticated():
    st.switch_page("pages/Login.py")

@st.fragment
def sync_status_fragment(user_id: str):
    """Fragment pour le statut et contrôles de synchronisation"""
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Statut de synchronisation
        status_icon, status_message = get_sync_status_display()
        st.write(f"{status_icon} {status_message}")
    
    with col2:
        # Bouton de synchronisation manuelle
        if st.button("☁️ Sync", help="Synchroniser avec le cloud", key="manual_sync_fragment"):
            with st.spinner("Synchronisation..."):
                success = sync_to_cloud(force=True)
                if success:
                    st.success("✅ Synchronisé!", icon="✅")
                else:
                    st.error("❌ Erreur sync", icon="❌")
                
                # Recharger seulement ce fragment
                time.sleep(0.5)
                st.rerun(scope="fragment")

@st.fragment
def csv_uploader_header_fragment(local_csv_path: str, remote_csv_path: str):
    """Fragment pour l'upload CSV header - se recharge indépendamment"""
    
    csv_uploader(
        filepath=local_csv_path,
        uploader_key="header_csv_controls_fragment",
        firebase_path=remote_csv_path,
        inline=True
    )

@st.fragment
def sync_details_sidebar_fragment():
    """Fragment pour les détails de sync dans la sidebar"""
    
    if 'sync_state' in st.session_state:
        sync_state = st.session_state.sync_state
        st.write(f"**Actions:** {sync_state['actions_count']}/10")
        
        if sync_state['last_sync_time']:
            last_sync = sync_state['last_sync_time'].strftime("%H:%M")
            st.write(f"**Dernière sync:** {last_sync}")
        else:
            st.write("**Dernière sync:** Jamais")
            
        # Barre de progression
        progress = min(sync_state['actions_count'] / 10, 1.0)
        st.progress(progress, text="Auto-sync:")

@st.fragment
def csv_uploader_sidebar_fragment(local_csv_path: str, remote_csv_path: str):
    """Fragment pour l'upload CSV sidebar - se recharge indépendamment"""
    
    csv_uploader(
        filepath=local_csv_path,
        title="Données Offres & Marché", 
        uploader_key="sidebar_data_controls_fragment",
        firebase_path=remote_csv_path
    )

def app():
    # 🔹 Identifiants utilisateur & chemins
    user_id = st.session_state.user["id"]
    
    # ✅ Initialiser le service de synchronisation
    initialize_sync_state(user_id)
    
    # ✅ Vérifier si une sync automatique est nécessaire (silencieuse)
    if should_auto_sync():
        sync_to_cloud(auto=True)  # Sans spinner pour ne pas perturber l'UX
    
    # ✅ CORRECTION : Distinction claire entre chemin distant et local
    remote_csv_path = get_market_offers_remote_path(user_id)  # Ex: "123/markets.csv"
    local_csv_path = get_market_offers_local_file(user_id)    # Ex: "data/tmp/user_123_markets.csv"
    
    # 🔹 Crée ou télécharge le fichier CSV si besoin
    ensure_market_file_exists(user_id)

    # 🔹 Cache géocodage
    if "geocoded_locations_cache" not in st.session_state:
        st.session_state.geocoded_locations_cache = load_cache()

    # ✅ Header avec fragments - Plus de rechargement complet !
    col1, col2 = st.columns([3, 1])
    
    with col1:
        csv_uploader_header_fragment(local_csv_path, remote_csv_path)
    
    with col2:
        sync_status_fragment(user_id)

    # 🔹 Interface principale
    st.title("JobCompass")
    
    # 🔍 DEBUG : Sections de debug (à supprimer en production)
    debug_auth()
    debug_supabase_auth()
    
    with st.sidebar:
        # ✅ Informations de synchronisation dans la sidebar avec fragment
        st.markdown("---")
        st.markdown("### 🔄 Synchronisation")
        
        sync_details_sidebar_fragment()
        
        st.markdown("---")
        
        csv_uploader_sidebar_fragment(local_csv_path, remote_csv_path)

    # Les onglets restent normaux (pas besoin de fragment ici)
    tabs = st.tabs(["🏠 Accueil", "📈 Analyse des marchés", "📝 Dissection des offres", "🧭 Boussole"])
    with tabs[0]: render_home()
    with tabs[1]: render_market_analysis()  # Maintenant avec fragments internes !
    with tabs[2]: render_offer_dissection()  # Maintenant avec fragments internes !
    with tabs[3]: render_compass()  # Maintenant avec fragments internes !

# ✅ Hook de déconnexion (si possible dans votre architecture)
def on_user_disconnect():
    """Appelé lors de la déconnexion utilisateur"""
    sync_on_disconnect()

app()
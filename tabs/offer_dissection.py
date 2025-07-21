import streamlit as st
import time
from pathlib import Path
from services.offers.get_all_existing_markets import get_all_existing_markets
from services.offers.get_existing_markets_from_offers import get_existing_markets_from_offers
from services.offers.save_offers import save_offer_data
from services.offers.load_offers import load_offers
from components.forms.offer_form import offer_form
from utils.filters import select_market_filter, filter_by_market_selection
from constants.alerts import SUCCESS_OFFER_SAVED, INFO_NO_OFFERS_DATA, INFO_NO_MARKET_FOR_OFFER_FORM
from constants.labels import HEADER_OFFER_DISSECTION, LABEL_DATA_SOURCE, SECTION_OFFERS_FORM, SECTION_OFFERS, LABEL_MARKET_FILTER, DATA_SOURCE_OPTIONS
from constants.schema.views import OFFER_DISPLAY_COLUMNS
from config.settings import get_market_offers_local_file
from services.sync.sync_service import mark_sync_action

@st.fragment
def offer_form_fragment(user_id: str, markets: list):
    """Fragment pour le formulaire d'ajout d'offre - se recharge indépendamment"""
    
    if not markets:
        st.info(INFO_NO_MARKET_FOR_OFFER_FORM)
        return
        
    source = st.radio(LABEL_DATA_SOURCE, DATA_SOURCE_OPTIONS, horizontal=True)
    offer_data = offer_form(markets, source=source)
    
    if offer_data:
        success = save_offer_data(offer_data, user_id)
        if success:
            # Marquer l'action pour la synchronisation
            mark_sync_action('offer_add')
            
            # Vider le cache
            if hasattr(st, 'cache_data'):
                st.cache_data.clear()
            
            st.success(SUCCESS_OFFER_SAVED)
            
            # ✅ FRAGMENT RERUN : Ne recharge que ce fragment
            st.rerun(scope="fragment")
            
        else:
            st.error("❌ Erreur lors de la sauvegarde de l'offre")

@st.fragment
def offers_display_fragment(user_id: str):
    """Fragment pour l'affichage des offres - se recharge indépendamment"""
    
    market_file = Path(get_market_offers_local_file(user_id))
    
    if not market_file.exists():
        st.info(INFO_NO_OFFERS_DATA)
        return
        
    # Chargement des données fraîches
    offers_df = load_offers(user_id)

    if offers_df.empty:
        st.info(INFO_NO_OFFERS_DATA)
        return

    # Filtre par marché
    markets_from_offers = get_existing_markets_from_offers(user_id)
    selected_market = select_market_filter(
        markets_from_offers, 
        LABEL_MARKET_FILTER, 
        key="offer_dissection_display_select"
    )
    
    filtered_df = filter_by_market_selection(offers_df, selected_market)
    
    # Affichage du tableau
    st.dataframe(filtered_df[OFFER_DISPLAY_COLUMNS], use_container_width=True)
    
    # Statistiques rapides
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total offres", len(filtered_df))
    with col2:
        if selected_market != "Tous les marchés":
            st.metric("Marché sélectionné", selected_market)
    with col3:
        if not filtered_df.empty and 'date' in filtered_df.columns:
            latest_date = filtered_df['date'].max() if pd.notna(filtered_df['date']).any() else "N/A"
            st.metric("Dernière offre", latest_date)

def render_offer_dissection():
    """Fonction principale - orchestration des fragments"""
    st.header(HEADER_OFFER_DISSECTION)

    user_id = st.session_state.user["id"]
    
    # ✅ Chargement initial des marchés (une seule fois)
    markets = get_all_existing_markets(user_id)

    # ✅ Fragment formulaire - se recharge indépendamment
    with st.expander(SECTION_OFFERS_FORM, expanded=True, icon=":material/forms_add_on:"):
        offer_form_fragment(user_id, markets)

    # ✅ Fragment affichage - se recharge indépendamment
    with st.expander(SECTION_OFFERS, expanded=True, icon=":material/business_center:"):
        offers_display_fragment(user_id)
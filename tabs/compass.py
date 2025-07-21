import streamlit as st
import pandas as pd
from services.offers.load_offers import load_offers
from services.market_analysis.load_markets_analysis import load_markets_analysis
from services.cache.geocoding_cache import save_cache
from components.maps.geocoding_feeback import geocode_with_feedback 
from components.charts.trend_chart import trend_chart
from components.charts.bar_chart import bar_chart
from components.charts.pie_chart import pie_chart
from components.numeric_range_slider import numeric_range_slider
from components.maps.offers_map import offers_map
from utils.filters import select_market_filter
from constants.alerts import (
    WARNING_MISSING_COLUMN, WARNING_NO_MARKET_ANALYSIS
)
from constants.labels import (
    HEADER_COMPASS, SECTION_MARKET_TRENDS, LABEL_TJM, LABEL_SENIORITY,
    LABEL_RHYTHM, LABEL_SECTOR, SECTION_POSITIONING, SECTION_MAP_OFFERS, SECTION_SKILLS, SECTION_TECHS,
    LABEL_MAIN_SKILLS, LABEL_SECONDARY_SKILLS, LABEL_MAIN_TECHS,
    LABEL_SECONDARY_TECHS, LABEL_SELECT_MARKET, TITLE_MARKET_TREND,
    X_AXIS_DATE, Y_AXIS_ADS, LEGEND_MARKET
)
from constants.schema.views import COMPASS_DISPLAY_COLUMNS
from constants.schema.columns import (
    COL_DATE, COL_MARKET, COL_SKILLS_MAIN, COL_SKILLS_SECONDARY,
    COL_TECHS_MAIN, COL_TECHS_SECONDARY, COL_TJM, COL_SENIORITY,
    COL_RHYTHM, COL_SECTOR, COL_NUMBER_OF_OFFERS, COL_LOCATION
)

@st.fragment
def market_selector_fragment(markets: list):
    """Fragment pour la sélection de marché avec communication globale"""
    
    # ✅ SOLUTION : Utiliser session_state pour la communication
    selected_market = select_market_filter(
        markets, 
        label=LABEL_SELECT_MARKET, 
        key="compass_market_select_fragment"
    )
    
    # ✅ Sauvegarder la sélection dans session_state
    if 'compass_selected_market' not in st.session_state:
        st.session_state.compass_selected_market = selected_market
    
    # ✅ Détecter le changement et forcer le rafraîchissement
    if st.session_state.compass_selected_market != selected_market:
        st.session_state.compass_selected_market = selected_market
        # Déclencher la mise à jour des autres fragments
        st.session_state.compass_market_changed = True
        st.rerun()
    
    return selected_market

@st.fragment
def market_trends_fragment(df_market_analysis: pd.DataFrame):
    """Fragment pour les tendances de marché - lit le marché depuis session_state"""
    
    # ✅ SOLUTION : Lire le marché sélectionné depuis session_state
    selected_market = st.session_state.get('compass_selected_market', 'Tous les marchés')
    
    trend_chart(
        df=df_market_analysis,
        index_col=COL_DATE,
        category_col=COL_MARKET,
        value_col=COL_NUMBER_OF_OFFERS,
        highlight=selected_market,
        title=TITLE_MARKET_TREND,
        x_axis_label=X_AXIS_DATE,
        y_axis_label=Y_AXIS_ADS,
        legend_title=LEGEND_MARKET,
        context_id="compass_trends_fragment"
    )

@st.fragment
def positioning_fragment(df_offers: pd.DataFrame):
    """Fragment pour le positionnement - filtre selon le marché sélectionné"""
    
    # ✅ SOLUTION : Filtrer selon le marché en session_state
    selected_market = st.session_state.get('compass_selected_market', 'Tous les marchés')
    
    if selected_market == "Tous les marchés":
        skills_df = df_offers.copy()  # ✅ CORRECTION : Copie explicite
    else:
        skills_df = df_offers[df_offers[COL_MARKET] == selected_market].copy()  # ✅ CORRECTION
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        numeric_range_slider(skills_df, COL_TJM, LABEL_TJM, unit="€")
    
    with col2:
        numeric_range_slider(skills_df, COL_SENIORITY, LABEL_SENIORITY, unit="ans")
    
    with col3:
        st.subheader(LABEL_RHYTHM)
        if not skills_df.empty and COL_RHYTHM in skills_df.columns:
            rhythm_data = skills_df[COL_RHYTHM].dropna().astype(str).str.strip()
            if not rhythm_data.empty:
                pie_chart(rhythm_data, title=LABEL_RHYTHM, context_id="compass_positioning_fragment")
            else:
                st.info("Aucune donnée de rythme disponible")
        else:
            st.info("Colonne rythme manquante")
    
    with col4:
        st.subheader(LABEL_SECTOR)
        if not skills_df.empty and COL_SECTOR in skills_df.columns:
            sector_data = skills_df[COL_SECTOR].dropna().astype(str).str.strip()
            if not sector_data.empty:
                pie_chart(sector_data, title=LABEL_SECTOR, context_id="compass_positioning_fragment")
            else:
                st.info("Aucune donnée de secteur disponible")
        else:
            st.info("Colonne secteur manquante")

@st.fragment
def map_offers_fragment(df_offers: pd.DataFrame):
    """Fragment pour la carte des offres - filtre selon le marché sélectionné"""
    
    # ✅ SOLUTION : Filtrer selon le marché en session_state
    selected_market = st.session_state.get('compass_selected_market', 'Tous les marchés')
    
    if selected_market == "Tous les marchés":
        skills_df = df_offers.copy()  # ✅ CORRECTION : Copie explicite
    else:
        skills_df = df_offers[df_offers[COL_MARKET] == selected_market].copy()  # ✅ CORRECTION
    
    offers_map(skills_df, selected_market)

@st.fragment
def skills_fragment(df_offers: pd.DataFrame):
    """Fragment pour les compétences - filtre selon le marché sélectionné"""
    
    # ✅ SOLUTION : Filtrer selon le marché en session_state
    selected_market = st.session_state.get('compass_selected_market', 'Tous les marchés')
    
    if selected_market == "Tous les marchés":
        skills_df = df_offers.copy()  # ✅ CORRECTION : Copie explicite
    else:
        skills_df = df_offers[df_offers[COL_MARKET] == selected_market].copy()  # ✅ CORRECTION
    
    # Compétences principales
    st.markdown(LABEL_MAIN_SKILLS)
    if not skills_df.empty and COL_SKILLS_MAIN in skills_df.columns:
        main_skills = skills_df[COL_SKILLS_MAIN].dropna().astype(str).str.split(",").explode().str.strip()
        if not main_skills.empty:
            bar_chart(
                main_skills,
                title=LABEL_MAIN_SKILLS,
                context_id="compass_skills_fragment"
            )
        else:
            st.info("Aucune compétence principale disponible")
    else:
        st.info("Colonne compétences principales manquante")
    
    # Compétences secondaires
    st.markdown(LABEL_SECONDARY_SKILLS)
    if not skills_df.empty and COL_SKILLS_SECONDARY in skills_df.columns:
        secondary_skills = skills_df[COL_SKILLS_SECONDARY].dropna().astype(str).str.split(",").explode().str.strip()
        if not secondary_skills.empty:
            bar_chart(
                secondary_skills,
                title=LABEL_SECONDARY_SKILLS,
                context_id="compass_skills_fragment"
            )
        else:
            st.info("Aucune compétence secondaire disponible")
    else:
        st.info("Colonne compétences secondaires manquante")

@st.fragment
def technologies_fragment(df_offers: pd.DataFrame):
    """Fragment pour les technologies - filtre selon le marché sélectionné"""
    
    # ✅ SOLUTION : Filtrer selon le marché en session_state
    selected_market = st.session_state.get('compass_selected_market', 'Tous les marchés')
    
    if selected_market == "Tous les marchés":
        skills_df = df_offers.copy()  # ✅ CORRECTION : Copie explicite
    else:
        skills_df = df_offers[df_offers[COL_MARKET] == selected_market].copy()  # ✅ CORRECTION
    
    # Technologies principales
    st.markdown(LABEL_MAIN_TECHS)
    if not skills_df.empty and COL_TECHS_MAIN in skills_df.columns:
        main_techs = skills_df[COL_TECHS_MAIN].dropna().astype(str).str.split(",").explode().str.strip()
        if not main_techs.empty:
            bar_chart(
                main_techs,
                title=LABEL_MAIN_TECHS,
                context_id="compass_technologies_fragment"
            )
        else:
            st.info("Aucune technologie principale disponible")
    else:
        st.info("Colonne technologies principales manquante")
    
    # Technologies secondaires
    st.markdown(LABEL_SECONDARY_TECHS)
    if not skills_df.empty and COL_TECHS_SECONDARY in skills_df.columns:
        secondary_techs = skills_df[COL_TECHS_SECONDARY].dropna().astype(str).str.split(",").explode().str.strip()
        if not secondary_techs.empty:
            bar_chart(
                secondary_techs,
                title=LABEL_SECONDARY_TECHS,
                context_id="compass_technologies_fragment"
            )
        else:
            st.info("Aucune technologie secondaire disponible")
    else:
        st.info("Colonne technologies secondaires manquante")

def render_compass():
    """Fonction principale - orchestration des fragments avec communication"""
    CONTEXT_ID = "compass"
    st.header(HEADER_COMPASS)

    user_id = st.session_state.user["id"]

    # ✅ Chargement initial des données (une seule fois)
    df_market_analysis = load_markets_analysis(user_id)
    df_offers_original = load_offers(user_id)
    
    # Géocodage avec feedback
    df_offers = geocode_with_feedback(
        df_offers_original, 
        COL_LOCATION, 
        st.session_state.geocoded_locations_cache
    )
    save_cache(st.session_state.geocoded_locations_cache)

    # Vérifications des données
    if df_offers.empty or any(col not in df_offers.columns for col in COMPASS_DISPLAY_COLUMNS):
        st.warning(WARNING_MISSING_COLUMN)
        return
        
    if COL_MARKET not in df_market_analysis.columns:
        st.warning(WARNING_NO_MARKET_ANALYSIS)
        return

    # Préparation des données
    markets = sorted(set(df_offers[COL_MARKET].dropna()) | set(df_market_analysis[COL_MARKET].dropna()))
    
    # ✅ Initialiser le marché par défaut si nécessaire
    if 'compass_selected_market' not in st.session_state:
        st.session_state.compass_selected_market = markets[0] if markets else "Tous les marchés"
    
    # ✅ Fragment sélecteur de marché (avec communication)
    selected_market = market_selector_fragment(markets)
    
    # ✅ Reset flag de changement après traitement
    if st.session_state.get('compass_market_changed', False):
        st.session_state.compass_market_changed = False

    # ✅ Fragment tendances des marchés
    with st.expander(SECTION_MARKET_TRENDS, expanded=True, icon=":material/insights:"):
        market_trends_fragment(df_market_analysis)

    # ✅ Fragment positionnement (reçoit les données brutes)
    with st.expander(SECTION_POSITIONING, expanded=True, icon=":material/my_location:"):
        positioning_fragment(df_offers)

    # ✅ Fragment localisation (reçoit les données brutes)
    with st.expander(SECTION_MAP_OFFERS, expanded=True, icon=":material/map:"):
        map_offers_fragment(df_offers)

    # ✅ Fragment compétences (reçoit les données brutes)
    with st.expander(SECTION_SKILLS, expanded=True, icon=":material/psychology:"):
        skills_fragment(df_offers)

    # ✅ Fragment technologies (reçoit les données brutes)
    with st.expander(SECTION_TECHS, expanded=True, icon=":material/settings_input_component:"):
        technologies_fragment(df_offers)
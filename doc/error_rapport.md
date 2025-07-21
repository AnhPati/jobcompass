##Erreur:

##Structure actuelle:
```
/job_compass
│
├── .streamlit/                                 # Réglages spécifiques à Streamlit
│   ├── config.toml                             # Configuration globale de Streamlit (thème, port, etc.)
│   └── secrets.toml                            # Fichier sécurisé contenant les identifiants (client_id, secrets, etc.)
|
├── Dockerfile
├── main.py                                    # Point d’entrée de l’app
├── menu.py
├── requirements.txt                            # Dépendances du projet
├── README.md                                   # Documentation
├── .env                                        # Ancienne gestion des secrets - @TODO : Migrer à terme tous les secrets vers secrets.toml
|
├── cache/                                      # Données stockées en cache local
│   └── geocoding_cache.json                    # Cache des géocodages effectués pour éviter les appels répétés à Nominatim
|
├── components/                                 # Composants UI réutilisables
│   ├── auth/                                   # Composants liés à l'authentification
│   │   ├── google_login.py                     # Gère le flux OAuth2 avec Google (provider)
│   │   └── login_form.py                       # Affiche l'UI de connexion selon mode fake ou prod
|   |
│   ├── charts/                                 # Composants de visualisation
│   │   ├── pie_chart.py                        # Diagrammes circulaires
│   │   ├── trend_chart.py                      # Graphiques temporels
│   │   └── bar_chart.py                        # Histogrammes
|   |
│   ├── forms/                                  # Composants de formulaire personnalisés
│   │   ├── config/
│   │   |   ├── offer_inputs.py                 # Configuration dynamique du formulaire d'offre
│   │   |   └── market_inputs.py                # Configuration dynamique du formulaire de marché
|   |   |
│   │   ├── market_form.py                      # Formulaire pour tendances de marché
│   │   └── offer_form.py                       # Formulaire pour offres ou contacts
|   |
│   ├── maps/                                   # Composants liés à la cartographie
│   │   ├── map_from_dataframe.py               # Affichage générique d'une carte
│   │   ├── offers_map.py                       # Carte dédiée aux offres géocodées
│   │   └── geocoding_feedback.py               # Composant UI de feedback pendant géocodage
|   |
│   ├── csv_uploader.py                         # Composant pour uploader des fichiers CSV
│   └── numeric_range_selector.py               # Composant pour explorer une valeur numérique
│
├── config/                                     # Fichiers de configuration globaux
│   ├── firebase_config.py                      # Paramètres pour initialiser Firebase (clé API, bucket, etc.)
│   ├── firebase_credentials.json               # Fichier JSON de service Firebase (si utilisé en local avec admin SDK)
│   └── settings.py                             # Configs globales (chemins, constantes, etc.)
│
├── constants/                                  # Constantes utilisées dans toute l’application
│   ├── schema/
│   |   ├── columns.py                          # Alias et noms de colonnes utilisés en interne
│   |   ├── constants.py                        # Constantes techniques : séparateur CSV, etc.
│   |   └── views.py                            # Colonnes affichées par vue (offres, compass, etc.)
|   |
│   ├── alerts.py                               # Messages utilisateur : erreurs, infos, succès
│   ├── labels.py                               # Libellés pour l’UI : champs, boutons, sections
│   └── texts.py                                # Textes d’introduction et de documentation
│
├── data/                                       # Fichiers CSV personnalisés de l’utilisateur
│   └── markets.csv                             # Données locales de l’utilisateur
│
├── design/                                     # Personnalisation de l’apparence
│   ├── inject_theme.py                         # Injecte dynamiquement un thème CSS dans l'app
│   ├── theme_colors.py                         # Palette de couleurs définie en Python
│   └── theme.css                               # Fichier CSS contenant le style complet à injecter
|
├── .devcontainer/
│   └── devcontainer.json
│
├── doc/                                        # Documentation du projet
│   ├── design.svg                              # Palette de couleurs de l'application
│   ├── folders-roles.png                       # @TODO : À supprimer si plus utilisé
│   └── structure.md                            # Ce fichier décrivant l’architecture du projet
|
├── pages/
│   ├── styles/
│   |   └── main.css
│   ├── Landing.py
│   ├── Login.py
│   ├── App.py
│   ├── admin.py
│   ├── super-admin.py
│   └── user.py
│
├── services/                                   # Couche "logique métier" – traitement des données
│   ├── cache/
│   │   └── geocoding_cache.py                  # Gère le chargement/sauvegarde du cache de géocodage
|   |
│   ├── mapping/
│   |   ├── client.py                           # Appels à l’API Nominatim
│   |   └── processor.py                        # Enrichissement de DataFrame avec coordonnées
|   |
│   ├── markets_analysis/
│   │   ├── load_markets_analysis.py            # Chargement des tendances de marché
│   │   └── save_markets_analysis.py            # Sauvegarde des données de marché
|   |
│   ├── offers/
│   │   ├── get_all_existing_markets.py # Récupération des marchés existants
│   │   ├── load_offers.py                      # Chargement des offres
│   │   └── save_offers.py                      # Sauvegarde d’une offre ou d’un contact
|   |
│   └── storage/
│       ├── append_to_market_file.py            # Ajout d’une ligne dans markets.csv
│       ├── supabase_storage_service.py         # Gère les échanges de fichiers avec Firebase Storage
│       ├── read_market_file.py                 # Lecture du fichier markets.csv
│       └── save_manager.py                     # Orchestration de sauvegardes (marché ou offres)
│
├── tabs/                                       # Pages principales de l’application
│   ├── compass.py                              # Logique + UI de l’onglet “Boussole”
│   ├── home.py                                 # Logique + UI de l’onglet “Accueil”
│   ├── market_analysis.py                      # Logique + UI de l’onglet “Analyse des marchés”
│   └── offer_dissection.py                     # Logique + UI de l’onglet “Dissection des offres”
│
└── utils/                                      # Utilitaires transverses
    ├── scripts/
    |   ├── csv.converter.py                    # Conversion d’anciens formats CSV vers le format unifié
    │   └── migrate_to_unified_markets.py       # Script de migration pour fusionner plusieurs fichiers de marché
    |
    ├── state/
    |   └── form_reset.py                       # Réinitialisation de formulaires dans session_state
    |
    ├── filters.py                              # Fonctions de filtrage et de sélection de marché
    ├── helpers.py                              # Fonctions utilitaires diverses
    ├── styling.py                              # Fonctions d’aide à la mise en forme (ex : colonnes colorées)
    └── validation.py                           # Vérifications de règles métier (unicité, etc.)
```

## Logs:
(venv) PS C:\Users\Usuario\Desktop\Taff\jobcompass> streamlit run main.py 

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.2.108:8501

[DEBUG] 📂 Vérification existence fichier : 548ac80b-256a-4bee-bd3a-6989989211d9/markets.csv
❌ Erreur lors de la vérification d'existence : SyncGoTrueClient.set_sessio
n() missing 1 required positional argument: 'refresh_token'
📂 Fichier 'user_548ac80b-256a-4bee-bd3a-6989989211d9_markets.csv' absent 
de Supabase. Création...
[DEBUG] 🔼 Tentative d'upload vers Supabase
[DEBUG] Chemin local : data\tmp\user_548ac80b-256a-4bee-bd3a-6989989211d9_markets.csv
[DEBUG] Chemin distant (remote_path) : '548ac80b-256a-4bee-bd3a-6989989211d9/markets.csv'
❌ Erreur lors de l'upload : SyncGoTrueClient.set_session() missing 1 requi
red positional argument: 'refresh_token'
[DEBUG] 📂 Vérification existence fichier : 548ac80b-256a-4bee-bd3a-6989989211d9/markets.csv
❌ Erreur lors de la vérification d'existence : SyncGoTrueClient.set_sessio
n() missing 1 required positional argument: 'refresh_token'
📂 Fichier 'user_548ac80b-256a-4bee-bd3a-6989989211d9_markets.csv' absent 
de Supabase. Création...
[DEBUG] 🔼 Tentative d'upload vers Supabase
[DEBUG] Chemin local : data\tmp\user_548ac80b-256a-4bee-bd3a-6989989211d9_markets.csv
[DEBUG] Chemin distant (remote_path) : '548ac80b-256a-4bee-bd3a-6989989211d9/markets.csv'
❌ Erreur lors de l'upload : SyncGoTrueClient.set_session() missing 1 requi
red positional argument: 'refresh_token'
[DEBUG] 🔼 Tentative d'upload vers Supabase
[DEBUG] Chemin local : <_io.BytesIO object at 0x000001B72CDD0C20>
[DEBUG] Chemin local : <_io.BytesIO object at 0x000001B72CDD0C20>
[DEBUG] Chemin distant (remote_path) : '548ac80b-256a-4bee-bd3a-6989989211d9/markets.csv'
❌ Erreur lors de l'upload : _path_exists: path should be string, bytes, osPathLike or integer, not BytesIO
.PathLike or integer, not BytesIO


## App.py:
```
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

# 🔹 Config Streamlit & Garde de sécurité
st.set_page_config(page_title="JobCompass", layout="wide")
inject_theme()

if not is_user_authenticated():
    st.switch_page("pages/Login.py")

def app():
    # 🔹 Identifiants utilisateur & chemins
    user_id = st.session_state.user["id"]
    
    # ✅ CORRECTION : Distinction claire entre chemin distant et local
    remote_csv_path = get_market_offers_remote_path(user_id)  # Ex: "123/markets.csv"
    local_csv_path = get_market_offers_local_file(user_id)    # Ex: "data/tmp/user_123_markets.csv"
    
    # 🔹 Crée ou télécharge le fichier CSV si besoin
    ensure_market_file_exists(user_id)

    # 🔹 Cache géocodage
    if "geocoded_locations_cache" not in st.session_state:
        st.session_state.geocoded_locations_cache = load_cache()

    # 🔹 Déconnexion + uploader dans header
    col1, col2 = st.columns([6, 1])
    with col1:
        csv_uploader(
            filepath=local_csv_path,              # ✅ CORRECTION : Utilise le chemin LOCAL
            uploader_key="header_csv_controls",
            firebase_path=remote_csv_path,        # ✅ CORRECTION : Utilise le chemin DISTANT
            inline=True
        )

    # 🔹 Interface principale
    st.title("JobCompass")
    with st.sidebar:
        csv_uploader(
            filepath=local_csv_path,              # ✅ CORRECTION : Utilise le chemin LOCAL
            title="Données Offres & Marché",
            uploader_key="sidebar_data_controls",
            firebase_path=remote_csv_path         # ✅ CORRECTION : Utilise le chemin DISTANT
        )

    tabs = st.tabs(["🏠 Accueil", "📈 Analyse des marchés", "📝 Dissection des offres", "🧭 Boussole"])
    with tabs[0]: render_home()
    with tabs[1]: render_market_analysis()
    with tabs[2]: render_offer_dissection()
    with tabs[3]: render_compass()

app()
```

## supabase_storage_service.py:
```
import tempfile
import os
from pathlib import Path
from supabase import create_client
import streamlit as st

# Configuration Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
SUPABASE_BUCKET = st.secrets.get("SUPABASE_BUCKET", "jobcompass-storage")

def get_authenticated_supabase_client():
    """
    Retourne un client Supabase authentifié avec le JWT de l'utilisateur
    """
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Récupérer le JWT de l'utilisateur connecté
    user = st.session_state.get("user")
    if not user:
        raise Exception("Utilisateur non connecté")
    
    # Essayer différentes clés pour le token
    jwt = (
        user.get("access_token") or
        user.get("accessToken") or 
        user.get("idToken") or
        st.session_state.get("access_token")
    )
    
    if not jwt:
        raise Exception("Token JWT non trouvé")
    
    # Définir le token d'authentification pour ce client
    supabase.auth.set_session(jwt)
    
    return supabase

def upload_csv_to_storage(file_path: str, remote_path: str) -> bool:
    """
    Upload un fichier CSV vers Supabase Storage avec authentification
    
    Args:
        file_path: Chemin vers le fichier local à uploader
        remote_path: Chemin de destination dans Supabase Storage
    
    Returns:
        bool: True si succès, False sinon
    """
    try:
        print(f"[DEBUG] 🔼 Tentative d'upload vers Supabase")
        print(f"[DEBUG] Chemin local : {file_path}")
        print(f"[DEBUG] Chemin distant (remote_path) : '{remote_path}'")
        
        # Vérifier que le fichier local existe
        if not os.path.exists(file_path):
            print(f"❌ Erreur : Le fichier {file_path} n'existe pas")
            return False
        
        # Obtenir le client authentifié
        supabase = get_authenticated_supabase_client()
        storage = supabase.storage
            
        # Supprimer l'ancien fichier s'il existe
        try:
            storage.from_(SUPABASE_BUCKET).remove([remote_path])
            print(f"🗑️ Ancien fichier '{remote_path}' supprimé avant upload.")
        except Exception as e:
            print(f"ℹ️ Pas d'ancien fichier à supprimer : {e}")

        # Lire le contenu du fichier
        with open(file_path, 'rb') as file:
            file_content = file.read()
            
        # Upload vers Supabase
        res = storage.from_(SUPABASE_BUCKET).upload(
            remote_path,
            file_content,
            file_options={"content-type": "text/csv"}
        )
        
        if hasattr(res, 'error') and res.error:
            print(f"❌ Erreur upload Supabase : {res.error}")
            return False
            
        print(f"✅ Upload réussi vers {remote_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'upload : {str(e)}")
        return False

def download_csv_from_storage(remote_path: str):
    """
    Télécharge un fichier CSV depuis Supabase Storage avec authentification
    
    Args:
        remote_path: Chemin du fichier dans Supabase Storage
    
    Returns:
        bytes: Contenu du fichier ou None si erreur
    """
    try:
        print(f"[DEBUG] 📥 Téléchargement depuis Supabase : {remote_path}")
        
        # Obtenir le client authentifié
        supabase = get_authenticated_supabase_client()
        storage = supabase.storage
        
        res = storage.from_(SUPABASE_BUCKET).download(remote_path)
        
        if res:
            print(f"✅ Téléchargement réussi de {remote_path}")
            return res
        else:
            print(f"❌ Échec du téléchargement de {remote_path}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement : {str(e)}")
        return None

def file_exists_in_storage(user_id: str) -> bool:
    """
    Vérifie si le fichier markets.csv existe pour un utilisateur
    
    Args:
        user_id: ID de l'utilisateur
    
    Returns:
        bool: True si le fichier existe, False sinon
    """
    try:
        remote_path = f"{user_id}/markets.csv"
        print(f"[DEBUG] 📂 Vérification existence fichier : {remote_path}")
        
        # Obtenir le client authentifié
        supabase = get_authenticated_supabase_client()
        storage = supabase.storage
        
        # Lister les fichiers dans le dossier utilisateur
        res = storage.from_(SUPABASE_BUCKET).list(user_id)
        
        if hasattr(res, 'error') and res.error:
            print(f"❌ Erreur lors de la vérification : {res.error}")
            return False
            
        # Chercher le fichier markets.csv
        for file_info in res:
            if file_info.get('name') == 'markets.csv':
                print(f"✅ Fichier trouvé : {remote_path}")
                return True
                
        print(f"📂 Fichier non trouvé : {remote_path}")
        return False
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification d'existence : {str(e)}")
        return False

def list_user_files(user_id: str) -> list:
    """
    Liste tous les fichiers d'un utilisateur
    
    Args:
        user_id: ID de l'utilisateur
    
    Returns:
        list: Liste des fichiers ou liste vide si erreur
    """
    try:
        print(f"[DEBUG] 📂 Contenu du dossier Supabase pour l'utilisateur '{user_id}' :")
        
        # Obtenir le client authentifié
        supabase = get_authenticated_supabase_client()
        storage = supabase.storage
        
        res = storage.from_(SUPABASE_BUCKET).list(user_id)
        
        if hasattr(res, 'error') and res.error:
            print(f"❌ Erreur lors du listage : {res.error}")
            return []
            
        files = []
        for file_info in res:
            filename = file_info.get('name', 'unknown')
            files.append(filename)
            print(f"📄 Fichier trouvé : {filename}")
            
        if not files:
            print(f"📂 Aucun fichier trouvé pour l'utilisateur {user_id}")
            
        return files
        
    except Exception as e:
        print(f"❌ Erreur lors du listage des fichiers : {str(e)}")
        return []

def get_user_jwt():
    """
    Récupère le JWT de l'utilisateur connecté
    """
    user = st.session_state.get("user")
    if not user:
        return None

    jwt = (
        user.get("access_token") or
        user.get("accessToken") or
        user.get("idToken") or
        st.session_state.get("access_token")
    )

    # @TODO : Vérifie aussi expiration du token ici si besoin
    if not jwt or jwt.strip() == "":
        return None

    return jwt
```

## market-file :
```
from pathlib import Path
import os

from config.settings import (
    get_market_offers_local_file,
    get_market_offers_remote_path,
)
from services.storage.supabase_storage_service import (
    file_exists_in_storage,
    upload_csv_to_storage,
    download_csv_from_storage,
)


def ensure_market_file_exists(user_id: str) -> None:
    # Détermination des chemins
    local_path = Path(get_market_offers_local_file(user_id))  # Exemple : data/tmp/user_123_markets.csv
    remote_path = get_market_offers_remote_path(user_id)      # Exemple : 123/markets.csv

    # Nom de fichier pour affichage
    file_name = local_path.name

    # Si le fichier n'existe pas dans le storage distant (Supabase)
    if not file_exists_in_storage(user_id):
        print(f"📂 Fichier '{file_name}' absent de Supabase. Création...")
        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_text("title,company,location,date\n", encoding="utf-8")
        upload_csv_to_storage(str(local_path), remote_path)
        return

    # Si le fichier existe sur Supabase mais pas en local
    if not local_path.exists():
        print(f"📥 Le fichier existe dans Supabase mais pas en local. Téléchargement...")
        file_content = download_csv_from_storage(remote_path)
        if file_content:
            local_path.parent.mkdir(parents=True, exist_ok=True)
            local_path.write_bytes(file_content.read())
        else:
            print(f"❌ Erreur : impossible de télécharger le fichier depuis Supabase.")
```

## settings.py :
from pathlib import Path

def get_market_offers_local_file(user_id: str) -> Path:
    return Path("data/tmp") / f"user_{user_id}_markets.csv"

def get_market_offers_remote_path(user_id: str) -> str:
    return f"{user_id}/markets.csv"

## offer_dissection.py :
import streamlit as st
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
from config.settings import get_market_offers_remote_path  # ✅ nouvelle méthode

def render_offer_dissection():
    st.header(HEADER_OFFER_DISSECTION)

    user_id = st.session_state.user["id"]
    markets = get_all_existing_markets(user_id)

    # ➕ Bloc collapsible pour l’ajout d’une offre/contact
    with st.expander(SECTION_OFFERS_FORM, expanded=True, icon=":material/forms_add_on:"):
        if not markets:
            st.info(INFO_NO_MARKET_FOR_OFFER_FORM)
        else:
            source = st.radio(LABEL_DATA_SOURCE, DATA_SOURCE_OPTIONS, horizontal=True)
            offer_data = offer_form(markets, source=source)
            if offer_data:
                save_offer_data(offer_data, user_id)
                st.success(SUCCESS_OFFER_SAVED)

    # 📄 Bloc collapsible pour l’affichage des offres enregistrées
    with st.expander(SECTION_OFFERS, expanded=True, icon=":material/business_center:"):
        market_file = Path(get_market_offers_remote_path(user_id))
        if market_file.exists():
            offers_df = load_offers(user_id)

            if offers_df.empty:
                st.info(INFO_NO_OFFERS_DATA)
                return

            markets_from_offers = get_existing_markets_from_offers(user_id)
            selected_market = select_market_filter(markets_from_offers, LABEL_MARKET_FILTER, key="offer_dissection_market_select")
            filtered_df = filter_by_market_selection(offers_df, selected_market)
            st.dataframe(filtered_df[OFFER_DISPLAY_COLUMNS])
        else:
            st.info(INFO_NO_OFFERS_DATA)

## compass.py :
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

def render_compass():
    CONTEXT_ID = "compass"
    st.header(HEADER_COMPASS)

    user_id = st.session_state.user["id"]

    df_market_analysis = load_markets_analysis(user_id)
    df_offers_original = load_offers(user_id)
    df_offers = geocode_with_feedback(df_offers_original, COL_LOCATION, st.session_state.geocoded_locations_cache)
    save_cache(st.session_state.geocoded_locations_cache)

    if df_offers.empty or any(col not in df_offers.columns for col in COMPASS_DISPLAY_COLUMNS):
        st.warning(WARNING_MISSING_COLUMN)
        return
    if COL_MARKET not in df_market_analysis.columns:
        st.warning(WARNING_NO_MARKET_ANALYSIS)
        return

    markets = sorted(set(df_offers[COL_MARKET].dropna()) | set(df_market_analysis[COL_MARKET].dropna()))
    selected_market = select_market_filter(markets, label=LABEL_SELECT_MARKET, key="compass_market_select")

    # 🔹 Tendance des marchés
    with st.expander(SECTION_MARKET_TRENDS, expanded=True, icon=":material/insights:"):
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
            context_id=CONTEXT_ID
        )

    skills_df = df_offers[df_offers[COL_MARKET] == selected_market]

    # 🔹 Positionnement
    with st.expander(SECTION_POSITIONING, expanded=True, icon=":material/my_location:"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            numeric_range_slider(skills_df, COL_TJM, LABEL_TJM, unit="€")
        with col2:
            numeric_range_slider(skills_df, COL_SENIORITY, LABEL_SENIORITY, unit="ans")
        with col3:
            st.subheader(LABEL_RHYTHM)
            pie_chart(skills_df[COL_RHYTHM].dropna().astype(str).str.strip(), title=LABEL_RHYTHM, context_id=CONTEXT_ID)
        with col4:
            st.subheader(LABEL_SECTOR)
            pie_chart(skills_df[COL_SECTOR].dropna().astype(str).str.strip(), title=LABEL_SECTOR, context_id=CONTEXT_ID)

    # 🔹 Localisation
    with st.expander(SECTION_MAP_OFFERS, expanded=True, icon=":material/map:"):
        offers_map(skills_df, selected_market)

    # 🔹 Compétences
    with st.expander(SECTION_SKILLS, expanded=True, icon=":material/psychology:"):
        st.markdown(LABEL_MAIN_SKILLS)
        bar_chart(
            skills_df[COL_SKILLS_MAIN].dropna().astype(str).str.split(",").explode().str.strip(),
            title=LABEL_MAIN_SKILLS,
            context_id=CONTEXT_ID
        )
        st.markdown(LABEL_SECONDARY_SKILLS)
        bar_chart(
            skills_df[COL_SKILLS_SECONDARY].dropna().astype(str).str.split(",").explode().str.strip(),
            title=LABEL_SECONDARY_SKILLS,
            context_id=CONTEXT_ID
        )

    # 🔹 Technologies
    with st.expander(SECTION_TECHS, expanded=True, icon=":material/settings_input_component:"):
        st.markdown(LABEL_MAIN_TECHS)
        bar_chart(
            skills_df[COL_TECHS_MAIN].dropna().astype(str).str.split(",").explode().str.strip(),
            title=LABEL_MAIN_TECHS,
            context_id=CONTEXT_ID
        )
        st.markdown(LABEL_SECONDARY_TECHS)
        bar_chart(
            skills_df[COL_TECHS_SECONDARY].dropna().astype(str).str.split(",").explode().str.strip(),
            title=LABEL_SECONDARY_TECHS,
            context_id=CONTEXT_ID
        )

## Policies Supabase Storage :
- SELECT : ((auth.uid() IS NOT NULL) AND (name = (auth.uid() || '/markets.csv'::text)))
- INSERT : ((auth.uid() IS NOT NULL) AND (name = (auth.uid() || '/markets.csv'::text)))
- UPDATE : ((auth.uid() IS NOT NULL) AND (name = (auth.uid() || '/markets.csv'::text)))
- DELETE : ((auth.uid() IS NOT NULL) AND (name = (auth.uid() || '/markets.csv'::text)))

## Contexte :

On cherche a affiché les informations en provenance du CSV uploadé.

## Problème :

Lorsque je téléverse mon csv, celui-ci affiche uniquement les infos dans Analyse des marchés.
Peux tu déjà analyser d'où vient le problème.
Si tu as besoin de plus de contexte n'hésite pas.
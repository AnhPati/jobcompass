import pandas as pd
import csv
import streamlit as st
from config.settings import get_market_offers_local_file
from utils.helpers import fallback_read_csv
from constants.alerts import ERROR_LOADING_MARKET_DATA
from constants.schema.constants import EXPECTED_COLUMNS, COLUMNS_SEP

def read_market_file():
    user_id = st.session_state.get("user_id")
    if not user_id:
        print("❌ Aucun utilisateur connecté.")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    local_file_path = get_market_offers_local_file(user_id)

    if not local_file_path.exists():
        print(f"[DEBUG] 📂 Aucun fichier trouvé à : {local_file_path}")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    try:
        df = pd.read_csv(
            local_file_path,
            sep=COLUMNS_SEP,
            quotechar=None,
            encoding='utf-8',
            header=0,
            engine='python',
            quoting=csv.QUOTE_NONE
        )
        print("[DEBUG] Colonnes chargées :", df.columns.tolist())
        print("[DEBUG] Premières lignes :", df.head(3))
        df = df.reindex(columns=EXPECTED_COLUMNS)
    except pd.errors.ParserError:
        df = fallback_read_csv(local_file_path, EXPECTED_COLUMNS)
    except Exception as e:
        print(ERROR_LOADING_MARKET_DATA.format(error=str(e)))
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    # Assurer que toutes les colonnes attendues sont présentes
    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = None

    return df
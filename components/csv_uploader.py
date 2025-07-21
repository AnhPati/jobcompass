import streamlit as st
import pandas as pd
import io
from pathlib import Path
from services.storage.supabase_storage_service import upload_csv_to_storage, download_csv_from_storage
from constants.alerts import *
from constants.labels import *
from constants.schema.columns import COL_TYPE
from constants.schema.constants import COLUMNS_SEP, EXPECTED_COLUMNS


def csv_uploader(filepath, uploader_key, title=None, expected_column=COL_TYPE,
                 firebase_path=None, inline=False, container=None):
    container = container or st
    user_id = st.session_state.user["id"]

    if not inline and title:
        container.markdown(f"### {LABEL_UPLOAD_SECTION.format(label=title)}")

    col1, col2 = container.columns([1, 1]) if inline else (container, container)
    file_uploader_kwargs = {
        "type": "csv",
        "key": f"{uploader_key}_upload",
        "label": BTN_UPLOAD_CSV if not inline else "Upload CSV",
        "label_visibility": "visible" if not inline else "collapsed",
    }

    uploaded_file = col1.file_uploader(**file_uploader_kwargs) if inline else container.file_uploader(**file_uploader_kwargs)

    if uploaded_file:
        container.info(f"✅ Fichier chargé : {uploaded_file.name} ({uploaded_file.size} octets)")
        try:
            df = pd.read_csv(
                uploaded_file,
                sep=COLUMNS_SEP,
                engine="python",
                quotechar='"',
                encoding="utf-8",
                header=0,
                on_bad_lines="skip"
            )
        except Exception as e:
            container.error("❌ Erreur lors de la lecture du fichier CSV.")
            container.exception(e)
            return

        if df.shape[1] != len(EXPECTED_COLUMNS):
            container.error(ERROR_INVALID_COLUMN_COUNT.format(
                dectected=df.shape[1], expected=len(EXPECTED_COLUMNS)))
            return

        if expected_column not in df.columns:
            container.error(ERROR_MISSING_TYPE_COLUMN)
            return

        df.columns = df.columns.map(str).str.strip()
        
        # ✅ CORRECTION 1 : Sauvegarder d'abord le fichier localement
        df.to_csv(filepath, sep="|", index=False)

        # ✅ CORRECTION 2 : Upload vers Supabase en utilisant le fichier local
        if firebase_path:
            print(f"[DEBUG] 🔼 Upload du fichier local vers Supabase")
            print(f"[DEBUG] Fichier local : {filepath}")
            print(f"[DEBUG] Chemin distant : {firebase_path}")
            
            # Utiliser directement le chemin du fichier local au lieu d'un BytesIO
            success = upload_csv_to_storage(str(filepath), firebase_path)
            
            if success:
                container.success(f"✅ {uploaded_file.name} → markets.csv uploadé vers Supabase !")
            else:
                container.warning("⚠️ Fichier sauvé localement, mais échec upload Supabase")
        
        container.success(SUCCESS_FILE_IMPORTED)

    # 📥 Bouton de téléchargement du fichier
    try:
        df_download = pd.read_csv(filepath, sep="|")
        buffer = io.StringIO()
        df_download.to_csv(buffer, index=False, sep="|")
        buffer.seek(0)

        download_target = col2 if inline else container
        download_target.download_button(
            label=f"📥 {BTN_DOWNLOAD_CSV}",
            data=buffer.getvalue(),
            file_name="markets.csv",  # ✅ CORRECTION 3 : Nom cohérent pour le téléchargement
            mime="text/csv",
            key=f"{uploader_key}_download"
        )
    except Exception as e:
        container.error("❌ Erreur lors de la préparation du fichier pour téléchargement.")
        container.exception(e)
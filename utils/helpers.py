import pandas as pd
import streamlit as st
from pathlib import Path
from typing import List

def initialize_session_state():
    if "user" not in st.session_state:
        st.session_state.user = None
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
    if "role" not in st.session_state:
        st.session_state.role = None

def is_user_authenticated() -> bool:
    jwt = get_user_jwt()
    return jwt is not None and jwt != ""

def get_user_jwt() -> str | None:
    # Vérifie dans access_token (session directe)
    jwt = st.session_state.get("access_token")
    
    # Sinon dans le bloc user
    user = st.session_state.get("user")
    if user:
        jwt = jwt or user.get("jwt") or user.get("access_token") or user.get("accessToken") or user.get("idToken")

    return jwt

def fallback_read_csv(file_path: Path, expected_columns: List[str]) -> pd.DataFrame:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip().split('|') for line in f.readlines()]

        cleaned_lines = []
        for line in lines:
            if len(line) == len(expected_columns):
                cleaned_lines.append(line)
            elif line:
                adjusted = line[:len(expected_columns)] + [''] * (len(expected_columns) - len(line))
                cleaned_lines.append(adjusted)

        if not cleaned_lines:
            return pd.DataFrame(columns=expected_columns)

        header = cleaned_lines[0]
        if len(header) != len(expected_columns):
            header = expected_columns

        return pd.DataFrame(cleaned_lines[1:], columns=header)

    except Exception as e:
        print(f"Erreur dans le fallback de lecture : {str(e)}")
        return pd.DataFrame(columns=expected_columns)
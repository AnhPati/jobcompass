import streamlit as st
import pandas as pd
from utils.styling import style_anchor

def numeric_range_slider(df: pd.DataFrame, column_name: str, title: str, unit: str = "") -> None:
    style_anchor(
        class_name="numeric-slider-block"
    )

    st.subheader(title)

    numeric_values = pd.to_numeric(df[column_name], errors='coerce').dropna()

    if numeric_values.empty:
        st.info("Aucune donnée numérique.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    min_val = int(numeric_values.min())
    max_val = int(numeric_values.max())
    avg_val = numeric_values.mean()

    st.markdown(f"**Moyenne :** {avg_val:,.0f}{unit}")
    st.markdown(f"**Fourchette :** {min_val} - {max_val}{unit}")

    unique_vals = sorted(numeric_values.unique())
    if len(unique_vals) > 1:
        default_val = min(unique_vals, key=lambda x: abs(x - avg_val))
        selected_val = st.select_slider(
            "Explorez les données par valeur :",
            options=unique_vals,
            value=default_val,
            format_func=lambda x: f"{x:,.0f}{unit}"
        )
        count = (numeric_values == selected_val).sum()
        st.markdown(f"**Nombre d'entrées à {selected_val:,.0f}{unit} :** {count}")
    elif len(unique_vals) == 1:
        val = unique_vals[0]
        count = numeric_values.count()
        st.markdown(f"**Valeur unique :** {val}{unit} ({count} occurrences)")
import streamlit as st
import pandas as pd
from collections import Counter
import plotly.express as px
from constants.labels import X_AXIS_SKILLS_TECH, Y_AXIS_FREQUENCY
from constants.alerts import INFO_NO_DATA_TO_DISPLAY
from design.theme_colors import THEME

def bar_chart(data, title="", context_id="default"):
    if data is None or not isinstance(data, pd.Series) or data.empty:
        st.info(INFO_NO_DATA_TO_DISPLAY)
        return

    counter = Counter(data)
    if not counter:
        st.info(INFO_NO_DATA_TO_DISPLAY)
        return

    sorted_items = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    labels, counts = zip(*sorted_items)

    fig = px.bar(
        x=labels,
        y=counts,
        labels={'x': X_AXIS_SKILLS_TECH, 'y': Y_AXIS_FREQUENCY},
        title=title
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        plot_bgcolor=THEME['surface'],      # 🔹 Fond de la zone de tracé
        paper_bgcolor=THEME['surface']      # 🔹 Fond du canevas global
    )

    st.plotly_chart(fig, use_container_width=True, key=f"bar_chart_{context_id}_{title or 'no_title'}")
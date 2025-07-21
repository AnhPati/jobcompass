import streamlit as st
import pandas as pd
from collections import Counter
import plotly.express as px
from utils.styling import style_anchor
from constants.alerts import INFO_NO_DATA_TO_DISPLAY

def pie_chart(data, title="", context_id="default"):
    style_anchor(
        class_name="pie-chart-block"
    )

    if data is None or not isinstance(data, pd.Series) or data.empty:
        st.info(INFO_NO_DATA_TO_DISPLAY)
        return

    counter = Counter(data)
    if not counter:
        st.info(INFO_NO_DATA_TO_DISPLAY)
        return

    sorted_items = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    labels, counts = zip(*sorted_items)

    fig = px.pie(
        values=counts,
        names=labels,
        title=title
    )
    st.plotly_chart(fig, use_container_width=True, key=f"pie_chart_{context_id}_{title or 'no_title'}")
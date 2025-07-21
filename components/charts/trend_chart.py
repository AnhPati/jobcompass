import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from constants.alerts import INFO_NO_DATA_TO_DISPLAY, INFO_NO_MARKET_DATA_AVAILABLE
from design.theme_colors import THEME

def trend_chart(
    df: pd.DataFrame,
    index_col: str,
    category_col: str,
    value_col: str,
    highlight: str | None = None,
    title: str = "",
    x_axis_label: str = "",
    y_axis_label: str = "",
    legend_title: str = "",
    context_id: str = "default"
):
    if df.empty:
        st.info(INFO_NO_DATA_TO_DISPLAY)
        return

    required_cols = [index_col, category_col, value_col]
    if not all(col in df.columns for col in required_cols):
        st.warning(INFO_NO_MARKET_DATA_AVAILABLE)
        return

    df = df.dropna(subset=required_cols)
    df[index_col] = pd.to_datetime(df[index_col], errors="coerce")
    df = df.dropna(subset=[index_col])

    if df.empty:
        st.warning(INFO_NO_MARKET_DATA_AVAILABLE)
        return

    pivot = df.pivot(index=index_col, columns=category_col, values=value_col).fillna(0)

    fig = go.Figure()
    for category in pivot.columns:
        is_highlighted = (category == highlight)
        fig.add_trace(go.Scatter(
            x=pivot.index,
            y=pivot[category],
            mode='lines',
            name=category,
            line=dict(
                width=4 if is_highlighted else 1,
                color='crimson' if is_highlighted else None,
                dash='solid' if is_highlighted else 'dot'
            ),
            opacity=1.0 if is_highlighted else 0.5
        ))

    fig.update_layout(
        title=title,
        xaxis_title=x_axis_label,
        yaxis_title=y_axis_label,
        legend_title=legend_title,
        template="plotly_white",
        hovermode="x unified",
        paper_bgcolor=THEME["surface"],
        plot_bgcolor=THEME["surface"],
        legend=dict(
            bgcolor=THEME["surface"],
            font=dict(color=THEME["text_secondary"]
                      )
        )
    )

    st.plotly_chart(fig, use_container_width=True, key=f"trend_chart_{context_id}_{highlight or 'default'}")
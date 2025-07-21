import streamlit as st
import pandas as pd
import plotly.express as px
from constants.alerts import INFO_NO_COORDINATES_DATA, INFO_MAP_SUMMARY
from constants.labels import LABEL_MAP_DETAIL, SECTION_MAP_OFFERS

def map_from_dataframe(
    df: pd.DataFrame,
    groupby_col: str,
    lat_col: str,
    lon_col: str,
    count_col_name: str = "Nombre",
    map_title: str = "",
    context_id: str = "map",
    market_name: str = ""
):
    st.subheader(SECTION_MAP_OFFERS)

    df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
    df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')

    grouped = df.groupby([groupby_col, lat_col, lon_col]).size().reset_index(name=count_col_name)
    grouped = grouped.dropna(subset=[lat_col, lon_col])

    if not grouped.empty:
        fig = px.scatter_mapbox(
            grouped,
            lat=lat_col,
            lon=lon_col,
            color=count_col_name,
            size=count_col_name,
            hover_name=groupby_col,
            hover_data={count_col_name: True, lat_col: False, lon_col: False},
            zoom=3,
            height=500,
            title=map_title,
            color_continuous_scale=px.colors.sequential.Plasma
        )
        fig.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)

        st.info(INFO_MAP_SUMMARY.format(
            n=len(grouped),
            s="s" if len(grouped) > 1 else "",
            market_name=market_name
        ))

        st.markdown(LABEL_MAP_DETAIL)
        st.dataframe(grouped.drop(columns=[lat_col, lon_col]).sort_values(by=count_col_name, ascending=False).reset_index(drop=True))
    else:
        st.info(INFO_NO_COORDINATES_DATA)
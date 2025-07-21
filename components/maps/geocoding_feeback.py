import streamlit as st
from services.mapping.processor import enrich_with_coordinates
from services.cache.geocoding_cache import save_cache
from constants.alerts import (
    ERROR_MISSING_LOCATION_COLUMN, INFO_GEOCODING_IN_PROGRESS,
    INFO_ALL_LOCATIONS_CACHED, SUCCESS_GEOCODING_DONE, INFO_GEOCODING_PROGRESS
)

def geocode_with_feedback(df, location_col, cache):
    if location_col not in df.columns:
        st.error(ERROR_MISSING_LOCATION_COLUMN.format(column=location_col))
        return df.copy()

    locations = df[location_col].dropna().unique()
    not_cached = [loc for loc in locations if loc not in cache]

    message = st.empty()
    progress = st.empty()

    if not_cached:
        message.info(INFO_GEOCODING_IN_PROGRESS.format(count=len(not_cached), s="s" if len(not_cached) > 1 else ""))
        bar = progress.progress(0, text=INFO_GEOCODING_PROGRESS)

        enriched_df = enrich_with_coordinates(df, location_col, cache)
        save_cache(cache)

        bar.progress(1.0, text=INFO_GEOCODING_PROGRESS)
        message.success(SUCCESS_GEOCODING_DONE)
        return enriched_df
    else:
        message.info(INFO_ALL_LOCATIONS_CACHED)
        return enrich_with_coordinates(df, location_col, cache)
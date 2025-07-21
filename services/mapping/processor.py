import pandas as pd
from .client import geocode_location

def enrich_with_coordinates(df: pd.DataFrame, location_col: str, cache: dict) -> pd.DataFrame:
    df = df.copy()
    if 'latitude' not in df.columns:
        df['latitude'] = None
    if 'longitude' not in df.columns:
        df['longitude'] = None

    unique_locations = df[location_col].dropna().unique()

    for loc in unique_locations:
        lat, lon = geocode_location(loc, cache)
        df.loc[df[location_col] == loc, 'latitude'] = lat
        df.loc[df[location_col] == loc, 'longitude'] = lon

    return df

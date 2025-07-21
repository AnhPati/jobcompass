import pandas as pd
from components.maps.map_from_dataframe import map_from_dataframe
from constants.schema.columns import COL_LOCATION, COL_NUMBER_OF_OFFERS 

def offers_map(df: pd.DataFrame, market_name: str):
    map_from_dataframe(
        df=df,
        groupby_col=COL_LOCATION,
        lat_col="latitude",
        lon_col="longitude",
        count_col_name=COL_NUMBER_OF_OFFERS,
        map_title=f"Nombre d'offres par localisation pour le marché '{market_name}'",
        context_id="offers_map",
        market_name=market_name
    )

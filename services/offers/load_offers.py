import pandas as pd
import csv
from pathlib import Path
from config.settings import get_market_offers_local_file  # ✅ CORRECTION : Chemin LOCAL
from utils.helpers import fallback_read_csv
from constants.alerts import ERROR_LOADING_OFFERS
from constants.schema.constants import EXPECTED_COLUMNS, COLUMNS_SEP
from constants.schema.columns import COL_TYPE

def load_offers(user_id: str) -> pd.DataFrame:
    # ✅ CORRECTION : Utiliser le chemin LOCAL au lieu du chemin distant
    market_file = Path(get_market_offers_local_file(user_id))

    if not market_file.exists():
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    try:
        df = pd.read_csv(
            market_file,
            sep=COLUMNS_SEP,
            quotechar=None,
            encoding='utf-8',
            header=0,
            engine='python',
            quoting=csv.QUOTE_NONE
        )
    except pd.errors.ParserError:
        df = fallback_read_csv(market_file, EXPECTED_COLUMNS)
    except Exception as e:
        print(ERROR_LOADING_OFFERS.format(error=str(e)))
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = None

    return df[df[COL_TYPE] == "Offre"].copy()
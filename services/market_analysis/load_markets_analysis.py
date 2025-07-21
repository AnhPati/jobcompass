import pandas as pd
import csv
from config.settings import get_market_offers_local_file
from utils.helpers import fallback_read_csv
from constants.alerts import ERROR_LOADING_MARKET_DATA
from constants.schema.constants import EXPECTED_COLUMNS, COLUMNS_SEP
from constants.schema.columns import COL_TYPE, COL_MARKET

def load_markets_analysis(user_id: str) -> pd.DataFrame:
    csv_path = get_market_offers_local_file(user_id)

    if not csv_path.exists():
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    try:
        df = pd.read_csv(
            csv_path,
            sep=COLUMNS_SEP,
            quotechar=None,
            encoding='utf-8',
            header=0,
            engine='python',
            quoting=csv.QUOTE_NONE
        )
    except pd.errors.ParserError:
        df = fallback_read_csv(csv_path, EXPECTED_COLUMNS)
    except Exception as e:
        print(ERROR_LOADING_MARKET_DATA.format(error=str(e)))
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = None

    return df[df[COL_TYPE] == COL_MARKET].copy()
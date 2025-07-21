import pandas as pd
from constants.alerts import ERROR_SAVING_MARKET_DATA
from constants.schema.constants import EXPECTED_COLUMNS

def save_markets_analysis(market_data: dict, filepath) -> bool:
    df = pd.DataFrame([market_data])

    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = None

    df = df[EXPECTED_COLUMNS]

    try:
        df.to_csv(
            filepath,
            sep="|",
            mode='a' if filepath.exists() else 'w',
            header=not filepath.exists(),
            index=False,
            encoding='utf-8',
            quoting=0
        )
        return True
    except Exception as e:
        print(ERROR_SAVING_MARKET_DATA.format(error=str(e)))
        return False
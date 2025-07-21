import pandas as pd
from pathlib import Path
from constants.schema.columns import COL_MARKET
from config.settings import get_market_offers_local_file  # ✅ CORRECTION : Chemin LOCAL

def get_all_existing_markets(user_id: str) -> list[str]:
    # ✅ CORRECTION : Utiliser le chemin LOCAL au lieu du chemin distant
    filepath = Path(get_market_offers_local_file(user_id))

    if not filepath.exists():
        return []

    try:
        df = pd.read_csv(filepath, sep="|")
        return sorted(df[COL_MARKET].dropna().unique())
    except Exception:
        return []
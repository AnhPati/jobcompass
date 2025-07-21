import pandas as pd
from pathlib import Path  # ✅ AJOUT : Import Path
from config.settings import get_market_offers_local_file  # ✅ CORRECTION : Utiliser local_file au lieu de remote_path
from constants.alerts import ERROR_SAVING_OFFERS
from constants.schema.constants import EXPECTED_COLUMNS

def save_offer_data(offer_data: dict | pd.DataFrame, user_id: str) -> bool:
    df = pd.DataFrame([offer_data]) if isinstance(offer_data, dict) else offer_data.copy()
    
    # ✅ CORRECTION : Utiliser le chemin LOCAL et le convertir en Path
    file_path = Path(get_market_offers_local_file(user_id))

    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = None

    df = df[EXPECTED_COLUMNS]

    try:
        df.to_csv(
            file_path,
            sep="|",
            mode='a' if file_path.exists() else 'w',
            header=not file_path.exists(),
            index=False,
            encoding='utf-8',
            quoting=0
        )
        return True
    except Exception as e:
        print(ERROR_SAVING_OFFERS.format(error=str(e)))
        return False
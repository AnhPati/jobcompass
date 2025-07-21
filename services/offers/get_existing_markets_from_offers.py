from constants.alerts import ERROR_LOADING_MARKETS_FROM_OFFERS
from constants.schema.columns import COL_MARKET
from services.offers.load_offers import load_offers

def get_existing_markets_from_offers(user_id: str) -> list[str]:
    try:
        df = load_offers(user_id)
        return sorted(df[COL_MARKET].dropna().astype(str).unique()) if not df.empty else []
    except Exception as e:
        print(ERROR_LOADING_MARKETS_FROM_OFFERS.format(error=str(e)))
        return []
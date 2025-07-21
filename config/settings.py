from pathlib import Path

def get_market_offers_local_file(user_id: str) -> Path:
    return Path("data/tmp") / f"user_{user_id}_markets.csv"

def get_market_offers_remote_path(user_id: str) -> str:
    return f"{user_id}/markets.csv"
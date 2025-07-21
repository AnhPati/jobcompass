import pandas as pd
from pathlib import Path

MARKET_ANALYSIS_FILE = Path("data/market_analysis.csv")
OFFERS_FILE = Path("data/offers.csv")
UNIFIED_FILE = Path("data/markets.csv")


def migrate() -> None:
    unified_rows = []

    if MARKET_ANALYSIS_FILE.exists():
        market_df = pd.read_csv(MARKET_ANALYSIS_FILE)
        for _, row in market_df.iterrows():
            unified_rows.append({
                "Date": row.get("Date", ""),
                "Marché": row.get("Marché", ""),
                "Nombre d'annonces": row.get("Nombre d'annonces", ""),
                "Notes": row.get("Notes", ""),
                **{field: "" for field in [
                    "Titre", "Intitulé", "TJM", "Séniorité",
                    "Technos principales", "Technos secondaires",
                    "Compétences principales", "Compétences secondaires",
                    "Secteur", "Localisation", "Rythme",
                    "Entreprise", "Contact", "Lien"
                ]}
            })

    if OFFERS_FILE.exists():
        offers_df = pd.read_csv(OFFERS_FILE)
        for _, row in offers_df.iterrows():
            unified_rows.append({
                "Date": "",
                "Marché": row.get("Marché", ""),
                "Nombre d'annonces": "",
                "Notes": "",
                "Titre": row.get("Titre", ""),
                "Intitulé": row.get("Intitulé", ""),
                "TJM": row.get("TJM", ""),
                "Séniorité": row.get("Séniorité", ""),
                "Technos principales": row.get("Technos principales", ""),
                "Technos secondaires": row.get("Technos secondaires", ""),
                "Compétences principales": row.get("Compétences principales", ""),
                "Compétences secondaires": row.get("Compétences secondaires", ""),
                "Secteur": row.get("Secteur", ""),
                "Localisation": row.get("Localisation", ""),
                "Rythme": row.get("Rythme", ""),
                "Entreprise": row.get("Entreprise", ""),
                "Contact": row.get("Contact", ""),
                "Lien": row.get("Lien", "")
            })

    pd.DataFrame(unified_rows).to_csv(UNIFIED_FILE, index=False)
    print(f"✅ Migration terminée : {len(unified_rows)} lignes écrites dans {UNIFIED_FILE}")


if __name__ == "__main__":
    migrate()
from pathlib import Path
from services.storage.supabase_storage_service import upload_csv_to_storage

# ⚠️ On pourra ajouter ici des règles plus complexes si besoin
def save_changes_if_any(local_path: Path, remote_path: str) -> None:
    """
    Uploade le fichier local vers Firebase Storage.
    À terme, on pourra conditionner cette opération (flag, timer, etc.)
    """
    if local_path.exists():
        upload_csv_to_storage(str(local_path), remote_path)
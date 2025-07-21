from pathlib import Path
import os

from config.settings import (
    get_market_offers_local_file,
    get_market_offers_remote_path,
)
from services.storage.supabase_storage_service import (
    file_exists_in_storage,
    upload_csv_to_storage,
    download_csv_from_storage,
)

def ensure_market_file_exists(user_id: str) -> None:
    """
    Logique de synchronisation intelligente :
    - Fichier local existe → Le conserver (priorité au local)
    - Fichier local absent + cloud existe → Récupérer du cloud
    - Aucun fichier → Créer nouveau
    """
    # Détermination des chemins
    local_path = Path(get_market_offers_local_file(user_id))  # Ex: data/tmp/user_123_markets.csv
    remote_path = get_market_offers_remote_path(user_id)      # Ex: 123/markets.csv

    # ✅ PRIORITÉ 1 : Si fichier local existe, le conserver
    if local_path.exists():
        print(f"✅ Fichier local trouvé : {local_path.name} (conservation)")
        return
    
    # ✅ PRIORITÉ 2 : Fichier local absent, vérifier le cloud
    print(f"📂 Fichier local absent, vérification cloud...")
    
    try:
        cloud_file_exists = file_exists_in_storage(user_id)
        
        if cloud_file_exists:
            # ✅ Cloud existe, local absent → Récupérer
            print(f"📥 Récupération depuis le cloud...")
            file_content = download_csv_from_storage(remote_path)
            
            if file_content:
                local_path.parent.mkdir(parents=True, exist_ok=True)
                with open(local_path, 'wb') as f:
                    f.write(file_content)
                print(f"✅ Fichier restauré depuis le cloud : {len(file_content)} bytes")
            else:
                print(f"❌ Échec téléchargement, création fichier vide")
                _create_empty_local_file(local_path)
        else:
            # ✅ Aucun fichier nulle part → Créer nouveau
            print(f"📂 Aucun fichier trouvé, création...")
            _create_empty_local_file(local_path)
            
            # Essayer de sauvegarder sur le cloud (non bloquant)
            try:
                upload_csv_to_storage(str(local_path), remote_path)
                print(f"✅ Nouveau fichier sauvegardé sur le cloud")
            except Exception as e:
                print(f"⚠️ Nouveau fichier créé localement seulement : {e}")
                
    except Exception as e:
        # ✅ Fallback : Assurer qu'un fichier local existe
        print(f"⚠️ Erreur cloud, création fichier local : {e}")
        _create_empty_local_file(local_path)

def _create_empty_local_file(local_path: Path):
    """Crée un fichier CSV vide avec les bonnes colonnes"""
    local_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Headers selon votre schéma
    headers = "title,company,location,date,type,market,skills_main,skills_secondary,techs_main,techs_secondary,tjm,seniority,rhythm,sector,number_of_offers,notes\n"
    
    local_path.write_text(headers, encoding="utf-8")
    print(f"✅ Fichier local créé : {local_path.name}")

def force_sync_cloud_to_local(user_id: str) -> bool:
    """
    Force la synchronisation cloud → local (SEULEMENT pour dépannage manuel)
    """
    try:
        local_path = Path(get_market_offers_local_file(user_id))
        remote_path = get_market_offers_remote_path(user_id)
        
        print(f"🔄 Force sync cloud → local (Manuel)...")
        
        file_content = download_csv_from_storage(remote_path)
        if file_content:
            # ✅ Backup du fichier local si il existe
            if local_path.exists():
                backup_path = local_path.with_suffix('.backup')
                local_path.rename(backup_path)
                print(f"📦 Backup local créé : {backup_path.name}")
            
            local_path.parent.mkdir(parents=True, exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(file_content)
            print(f"✅ Force sync réussie : {len(file_content)} bytes")
            return True
        else:
            print(f"❌ Force sync échouée - aucun fichier cloud")
            return False
            
    except Exception as e:
        print(f"❌ Erreur force sync : {e}")
        return False

def force_sync_local_to_cloud(user_id: str) -> bool:
    """
    Force la synchronisation local → cloud (pour sauvegarde manuelle)
    """
    try:
        local_path = Path(get_market_offers_local_file(user_id))
        remote_path = get_market_offers_remote_path(user_id)
        
        if not local_path.exists():
            print(f"❌ Aucun fichier local à sauvegarder")
            return False
            
        print(f"🔄 Force sync local → cloud (Manuel)...")
        
        success = upload_csv_to_storage(str(local_path), remote_path)
        if success:
            print(f"✅ Force sync réussie vers le cloud")
            return True
        else:
            print(f"❌ Force sync échouée vers le cloud")
            return False
            
    except Exception as e:
        print(f"❌ Erreur force sync : {e}")
        return False
import streamlit as st
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

# ✅ Configuration centralisée
SYNC_CONFIG = {
    'actions_threshold': 10,      # Sync après 10 actions
    'inactive_minutes': 15,       # Sync après 15 min d'inactivité
    'browser_backup_frequency': 5  # Backup browser toutes les 5 actions
}

def initialize_sync_state(user_id: str):
    """Initialise l'état de synchronisation pour l'utilisateur"""
    if 'sync_state' not in st.session_state:
        st.session_state.sync_state = {
            'user_id': user_id,
            'actions_count': 0,
            'last_action_time': datetime.now(),
            'last_sync_time': None,
            'pending_changes': False,
            'sync_status': 'synced'  # 'synced', 'pending', 'error'
        }
        
        # Setup browser backup
        _setup_browser_backup()

def _setup_browser_backup():
    """Configure le backup automatique dans le navigateur"""
    browser_backup_js = """
    <script>
    function backupToLocalStorage(data, key) {
        try {
            localStorage.setItem('jobcompass_' + key, JSON.stringify(data));
            console.log('✅ Backup browser:', key);
        } catch(e) {
            console.warn('⚠️ Backup browser échoué:', e);
        }
    }
    
    function restoreFromLocalStorage(key) {
        try {
            const data = localStorage.getItem('jobcompass_' + key);
            return data ? JSON.parse(data) : null;
        } catch(e) {
            console.warn('⚠️ Restauration browser échouée:', e);
            return null;
        }
    }
    
    function cleanOldBackups() {
        const weekAgo = Date.now() - (7 * 24 * 60 * 60 * 1000);
        for(let i = localStorage.length - 1; i >= 0; i--) {
            const key = localStorage.key(i);
            if(key && key.startsWith('jobcompass_backup_')) {
                const timestamp = parseInt(key.split('_').pop());
                if(timestamp < weekAgo) {
                    localStorage.removeItem(key);
                }
            }
        }
    }
    </script>
    """
    st.components.v1.html(browser_backup_js, height=0)

def mark_sync_action(action_type: str = "data_change"):
    """Marque qu'une action nécessitant une sync a été effectuée"""
    if 'sync_state' not in st.session_state:
        return
        
    sync_state = st.session_state.sync_state
    sync_state['actions_count'] += 1
    sync_state['last_action_time'] = datetime.now()
    sync_state['pending_changes'] = True
    sync_state['sync_status'] = 'pending'
    
    print(f"[SYNC] Action #{sync_state['actions_count']}: {action_type}")
    
    # Backup browser pour actions critiques
    if action_type in ['market_add', 'offer_add']:
        _backup_to_browser(sync_state['user_id'])
    
    # Auto-sync si seuil atteint
    if sync_state['actions_count'] >= SYNC_CONFIG['actions_threshold']:
        print(f"[SYNC] Seuil atteint - Auto-sync")
        sync_to_cloud(auto=True)

def _backup_to_browser(user_id: str):
    """Backup des données critiques dans le navigateur"""
    try:
        from config.settings import get_market_offers_local_file
        import pandas as pd
        
        local_file = get_market_offers_local_file(user_id)
        if not Path(local_file).exists():
            return
            
        # Lire et préparer les données
        df = pd.read_csv(local_file, sep="|")
        backup_data = {
            'timestamp': int(time.time()),
            'user_id': user_id,
            'data': df.to_dict('records')[:100],  # Limite pour performance
            'total_rows': len(df)
        }
        
        # JavaScript pour sauvegarder
        backup_js = f"""
        <script>
        backupToLocalStorage({json.dumps(backup_data)}, 'backup_{int(time.time())}');
        </script>
        """
        st.components.v1.html(backup_js, height=0)
        print(f"[SYNC] ✅ Backup browser ({len(df)} lignes)")
        
    except Exception as e:
        print(f"[SYNC] ⚠️ Backup browser échoué: {e}")

def should_auto_sync() -> bool:
    """Détermine si une synchronisation automatique est nécessaire"""
    if 'sync_state' not in st.session_state:
        return False
        
    sync_state = st.session_state.sync_state
    
    if not sync_state['pending_changes']:
        return False
        
    # Sync par nombre d'actions
    if sync_state['actions_count'] >= SYNC_CONFIG['actions_threshold']:
        return True
        
    # Sync par inactivité
    last_action = sync_state['last_action_time']
    inactive_time = datetime.now() - last_action
    if inactive_time > timedelta(minutes=SYNC_CONFIG['inactive_minutes']):
        return True
        
    return False

def sync_to_cloud(force: bool = False, auto: bool = False) -> bool:
    """Synchronise les données locales avec Supabase Storage"""
    if 'sync_state' not in st.session_state:
        return False
        
    sync_state = st.session_state.sync_state
    
    # Vérifier si sync nécessaire
    if not force and not auto and not should_auto_sync():
        return True
        
    try:
        from services.storage.supabase_storage_service import upload_csv_to_storage
        from config.settings import get_market_offers_local_file, get_market_offers_remote_path
        
        user_id = sync_state['user_id']
        local_file = get_market_offers_local_file(user_id)
        remote_path = get_market_offers_remote_path(user_id)
        
        if not Path(local_file).exists():
            print("[SYNC] ⚠️ Pas de fichier local à synchroniser")
            return True
            
        print(f"[SYNC] 🔄 Synchronisation {'(auto)' if auto else '(manuelle)'}")
        
        success = upload_csv_to_storage(str(local_file), remote_path)
        
        if success:
            # Réinitialiser les compteurs
            sync_state['actions_count'] = 0
            sync_state['last_sync_time'] = datetime.now()
            sync_state['pending_changes'] = False
            sync_state['sync_status'] = 'synced'
            
            print("[SYNC] ✅ Synchronisation réussie")
            return True
        else:
            sync_state['sync_status'] = 'error'
            print("[SYNC] ❌ Synchronisation échouée")
            return False
            
    except Exception as e:
        st.session_state.sync_state['sync_status'] = 'error'
        print(f"[SYNC] ❌ Erreur: {e}")
        return False

def get_sync_status_display() -> tuple[str, str]:
    """Retourne l'icône et le message pour l'affichage du statut"""
    if 'sync_state' not in st.session_state:
        return '🟢', 'Synchronisé'
        
    sync_state = st.session_state.sync_state
    status = sync_state['sync_status']
    actions_count = sync_state['actions_count']
    
    status_map = {
        'synced': ('🟢', 'Synchronisé'),
        'pending': ('🟡', f'Modifications locales ({actions_count})'),
        'error': ('🔴', 'Erreur sync')
    }
    
    return status_map.get(status, ('🟢', 'Synchronisé'))

def sync_on_disconnect():
    """Effectue une synchronisation forcée lors de la déconnexion"""
    if 'sync_state' in st.session_state and st.session_state.sync_state['pending_changes']:
        print("[SYNC] 🔄 Sync de déconnexion...")
        sync_to_cloud(force=True)

# ✅ Usage simple dans votre app :
def handle_market_added():
    """Appelé après qu'un marché a été ajouté"""
    mark_sync_action('market_add')

def handle_offer_added():
    """Appelé après qu'une offre a été ajoutée"""
    mark_sync_action('offer_add')
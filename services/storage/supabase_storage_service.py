import requests
import os
import streamlit as st

# Configuration Supabase
from utils.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_BUCKET

def get_auth_headers():
    """
    Récupère les headers d'authentification pour les API Supabase
    """
    user = st.session_state.get("user")
    if not user:
        raise Exception("Utilisateur non connecté")
    
    jwt = user.get("jwt")
    if not jwt:
        raise Exception("Token JWT non trouvé")
    
    return {
        'Authorization': f'Bearer {jwt}',
        'apikey': SUPABASE_KEY,
        'Content-Type': 'application/json'
    }

def upload_csv_to_storage_direct(file_path: str, remote_path: str) -> bool:
    """
    Upload un fichier CSV vers Supabase Storage via API REST directe
    """
    try:
        print(f"[DEBUG] 🔼 Upload direct via API REST")
        print(f"[DEBUG] Chemin local : {file_path}")
        print(f"[DEBUG] Chemin distant : '{remote_path}'")
        
        # Lire le contenu du fichier
        if hasattr(file_path, 'read'):  # BytesIO
            file_content = file_path.read()
            file_path.seek(0)
        elif os.path.exists(str(file_path)):  # Chemin fichier
            with open(file_path, 'rb') as f:
                file_content = f.read()
        else:
            print(f"❌ Erreur : Le fichier {file_path} n'existe pas")
            return False
        
        # Headers d'authentification
        headers = get_auth_headers()
        headers['Content-Type'] = 'text/csv'
        
        # URL pour l'upload
        upload_url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{remote_path}"
        
        # Supprimer l'ancien fichier s'il existe
        try:
            delete_url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{remote_path}"
            delete_response = requests.delete(delete_url, headers=get_auth_headers())
            if delete_response.status_code in [200, 204]:
                print(f"🗑️ Ancien fichier supprimé")
            else:
                print(f"ℹ️ Pas d'ancien fichier à supprimer (status: {delete_response.status_code})")
        except:
            print(f"ℹ️ Erreur suppression (normal si fichier inexistant)")
        
        # Upload du fichier - si erreur "Duplicate", essayer avec PUT (update)
        response = requests.post(upload_url, data=file_content, headers=headers)
        
        # Si erreur "Duplicate", essayer une mise à jour au lieu d'une création
        if response.status_code == 400 and "already exists" in response.text.lower():
            print(f"🔄 Fichier existant détecté, tentative de mise à jour...")
            # Utiliser PUT pour mettre à jour le fichier existant
            response = requests.put(upload_url, data=file_content, headers=headers)
        
        if response.status_code in [200, 201]:
            print(f"✅ Upload réussi vers {remote_path}")
            return True
        else:
            print(f"❌ Erreur upload : {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'upload direct : {str(e)}")
        return False

def download_csv_from_storage_direct(remote_path: str):
    """
    Télécharge un fichier CSV depuis Supabase Storage via API REST directe
    """
    try:
        print(f"[DEBUG] 📥 Download direct via API REST : {remote_path}")
        
        # URL pour le download
        download_url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{remote_path}"
        
        # Headers d'authentification
        headers = get_auth_headers()
        
        response = requests.get(download_url, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ Téléchargement réussi de {remote_path}")
            return response.content
        else:
            print(f"❌ Erreur téléchargement : {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement direct : {str(e)}")
        return None

def file_exists_in_storage_direct(user_id: str) -> bool:
    """
    Vérifie si le fichier markets.csv existe pour un utilisateur via API REST
    """
    try:
        remote_path = f"{user_id}/markets.csv"
        print(f"[DEBUG] 📂 Vérification existence via API REST : {remote_path}")
        
        # Méthode 1 : Essayer de télécharger directement le fichier
        download_url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{remote_path}"
        headers = get_auth_headers()
        
        response = requests.head(download_url, headers=headers)  # HEAD au lieu de GET pour juste vérifier l'existence
        
        if response.status_code == 200:
            print(f"✅ Fichier trouvé : {remote_path}")
            return True
        elif response.status_code == 404:
            print(f"📂 Fichier non trouvé : {remote_path}")
            return False
        else:
            print(f"⚠️ Status inattendu lors de la vérification : {response.status_code}")
            # Fallback : considérer que le fichier n'existe pas
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification directe : {str(e)}")
        return False

# Fonctions de compatibilité (garde les mêmes noms)
def upload_csv_to_storage(file_path: str, remote_path: str) -> bool:
    return upload_csv_to_storage_direct(file_path, remote_path)

def download_csv_from_storage(remote_path: str):
    return download_csv_from_storage_direct(remote_path)

def file_exists_in_storage(user_id: str) -> bool:
    return file_exists_in_storage_direct(user_id)
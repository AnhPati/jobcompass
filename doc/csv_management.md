# 🧾 Gestion du fichier CSV utilisateur avec Supabase

## ✅ Cas d’usage : que faire à chaque étape

---

### 1. Chargement d’un CSV par l’utilisateur (upload depuis son poste)

**✅ À faire :**
- Sauvegarder le fichier **localement en temporaire** (`data/tmp/...`).
- Puis **l’uploader dans Supabase** immédiatement.

> Cela évite que le fichier ne reste seulement en local.  
> Si l’utilisateur recharge la page ou change de machine, il retrouve bien ses données.

---

### 2. Téléchargement du fichier CSV (download vers son poste)

**✅ À faire :**
- Télécharger **le fichier depuis Supabase vers un fichier temporaire local**.
- Puis le fournir en téléchargement à l’utilisateur.

> Pas besoin d’uploader vers le cloud si le fichier venait déjà de là.  
> On ne fait que *servir* un fichier déjà présent dans Supabase.

---

### 3. Modification du CSV (ex: via formulaire ou interface)

**✅ À faire :**
- Modifier le **fichier local temporaire**.
- Puis **re-uploader** dans Supabase une fois les modifications faites.

> Cela évite que les modifications restent seulement côté session locale ou RAM.  
> Tu peux uploader automatiquement après chaque modif, ou quand l’utilisateur clique sur un bouton "sauvegarder".

---

### 4. Fin de session ou fermeture de l’application

**✅ À faire :**
- Supprimer les fichiers temporaires (`data/tmp/`) pour éviter de polluer le disque local.
- **Pas besoin de re-sauvegarder** dans Supabase **si tu l’as déjà fait avant**.

> Mais si tu **n’as pas encore sauvegardé**, alors **il faut le faire avant de supprimer**.

---

## ✅ Résumé des actions à mettre en place

| Étape                            | Temp local | Supabase | À faire                                                                |
|----------------------------------|------------|----------|------------------------------------------------------------------------|
| Upload CSV                       | ✅ Oui      | ✅ Oui    | Stocker temporairement et uploader                                     |
| Télécharger CSV                  | ✅ Oui      | ❌ Non    | Télécharger depuis Supabase vers local temp, puis download utilisateur |
| Modifier CSV                     | ✅ Oui      | ✅ Oui    | Écrire en local et re-uploader                                         |
| Fin de session                   | ❌ Non      | ✅ Oui    | Supprimer local si déjà sauvegardé                                     |

---

## 🛠️ À implémenter

Tu peux ajouter :
- Une fonction `cleanup_tmp_files()`
- Un wrapper `save_and_cleanup(user_id: str)` qui upload puis supprime si besoin

---

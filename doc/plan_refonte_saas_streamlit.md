
# 🧭 Plan de Refonte SaaS avec Streamlit SaaS Starter

## ✅ Objectifs

- Intégrer le template `streamlit-saas-starter`
- Migrer Firebase vers Supabase **si nécessaire**
- Conserver l’approche actuelle avec CSV si elle reste simple et viable
- Structurer l’app pour devenir un produit SaaS avec authentification, page de vente, paiement

---

## 🧱 1. Installer et comprendre `streamlit-saas-starter`

### Étapes :
- Cloner [`streamlit-saas-starter`](https://github.com/antoineross/streamlit-saas-starter)
- Installer localement et tester :
  ```bash
  poetry install  # ou pip install -r requirements.txt
  streamlit run Home.py
  ```
- Vérifier :
  - Auth Google via Supabase
  - Structure `pages/`, `app/`, `config/` bien comprise

---

## ⚠️ Auth Google et Streamlit Cloud

- Problème initial : Firebase n’autorise pas les redirections dynamiques de Streamlit Cloud
- Avantage du starter : utilise Supabase Auth **sans redirection frontend**
- ✅ Avec le starter, l’auth Google fonctionne sur Streamlit Cloud si bien configurée

---

## 🧩 2. Intégrer ton code actuel dans la structure du starter

Ta logique actuelle (chargement CSV, affichage des tendances, etc.) doit être migrée dans :
```
.
├── Home.py
├── app/
│   ├── pages/               # ex : dashboard.py
│   ├── components/          # composants réutilisables
│   └── services/            # accès données, CSV ou Supabase
```
👉 Migration simple à faire une fois ton script principal intégré.

---

## 🛠 3. Migrer Firebase → Supabase (optionnel)

### À faire si :
- Tu veux rester sur Streamlit Cloud
- Tu veux tout centraliser (auth + stockage + base)

### Supabase permet :
- Auth Google
- Stockage des fichiers (CSV, etc.)
- Base relationnelle (ou JSON)

---

## 💸 4. Page de vente & paiements

Le starter inclut déjà :
- Page d’accueil (`Home.py`)
- Connexion / inscription
- Intégration Stripe (plans, abonnements, webhooks)

À configurer :
- Ton compte Stripe + clés `.env`
- Ton plan dans Stripe Dashboard
- Gestion des droits utilisateurs (`plan`, `is_premium`, etc.)

---

## 🚦 Ordre d’implémentation recommandé

| Étape | Action | Durée estimée |
|------|--------|----------------|
| ✅ Étape 1 | Cloner et tester `streamlit-saas-starter` en local | 1h |
| ✅ Étape 2 | Créer projet Supabase (auth + table users) | 30min |
| ✅ Étape 3 | Vérifier auth Google sur Streamlit Cloud | 15min |
| 🟡 Étape 4 | Migrer dashboard Streamlit dans `pages/dashboard.py` | 1 demi-journée |
| 🟡 Étape 5 | Ajouter l’upload CSV (via Supabase Storage si besoin) | 1h |
| 🔜 Étape 6 | Ajouter page "Plan d’apprentissage" ou "Tendances" | 1–2j |
| 🔜 Étape 7 | Configurer Stripe pour les accès premium | 1j |

---

## 📦 Aide possible

- Initialiser proprement ton projet avec le starter
- Rebrancher CSV sur Supabase
- Créer les tables si sortie du CSV envisagée
- Adapter ton dashboard à la nouvelle structure
- Ajouter authentification et paiements

➡️ Tu peux commencer dès maintenant par l’installation du starter.

/job_compass
│
├── .streamlit/                                 # Réglages spécifiques à Streamlit
│   ├── config.toml                             # Configuration globale de Streamlit (thème, port, etc.)
│   └── secrets.toml                            # Fichier sécurisé contenant les identifiants (client_id, secrets, etc.)
|
├── Dockerfile
├── main.py                                    # Point d’entrée de l’app
├── menu.py
├── requirements.txt                            # Dépendances du projet
├── README.md                                   # Documentation
├── .env                                        # Ancienne gestion des secrets - @TODO : Migrer à terme tous les secrets vers secrets.toml
|
├── cache/                                      # Données stockées en cache local
│   └── geocoding_cache.json                    # Cache des géocodages effectués pour éviter les appels répétés à Nominatim
|
├── components/                                 # Composants UI réutilisables
│   ├── auth/                                   # Composants liés à l'authentification
│   │   ├── google_login.py                     # Gère le flux OAuth2 avec Google (provider)
│   │   └── login_form.py                       # Affiche l'UI de connexion selon mode fake ou prod
|   |
│   ├── charts/                                 # Composants de visualisation
│   │   ├── pie_chart.py                        # Diagrammes circulaires
│   │   ├── trend_chart.py                      # Graphiques temporels
│   │   └── bar_chart.py                        # Histogrammes
|   |
│   ├── forms/                                  # Composants de formulaire personnalisés
│   │   ├── config/
│   │   |   ├── offer_inputs.py                 # Configuration dynamique du formulaire d'offre
│   │   |   └── market_inputs.py                # Configuration dynamique du formulaire de marché
|   |   |
│   │   ├── market_form.py                      # Formulaire pour tendances de marché
│   │   └── offer_form.py                       # Formulaire pour offres ou contacts
|   |
│   ├── maps/                                   # Composants liés à la cartographie
│   │   ├── map_from_dataframe.py               # Affichage générique d'une carte
│   │   ├── offers_map.py                       # Carte dédiée aux offres géocodées
│   │   └── geocoding_feedback.py               # Composant UI de feedback pendant géocodage
|   |
│   ├── csv_uploader.py                         # Composant pour uploader des fichiers CSV
│   └── numeric_range_selector.py               # Composant pour explorer une valeur numérique
│
├── config/                                     # Fichiers de configuration globaux
│   ├── firebase_config.py                      # Paramètres pour initialiser Firebase (clé API, bucket, etc.)
│   ├── firebase_credentials.json               # Fichier JSON de service Firebase (si utilisé en local avec admin SDK)
│   └── settings.py                             # Configs globales (chemins, constantes, etc.)
│
├── constants/                                  # Constantes utilisées dans toute l’application
│   ├── schema/
│   |   ├── columns.py                          # Alias et noms de colonnes utilisés en interne
│   |   ├── constants.py                        # Constantes techniques : séparateur CSV, etc.
│   |   └── views.py                            # Colonnes affichées par vue (offres, compass, etc.)
|   |
│   ├── alerts.py                               # Messages utilisateur : erreurs, infos, succès
│   ├── labels.py                               # Libellés pour l’UI : champs, boutons, sections
│   └── texts.py                                # Textes d’introduction et de documentation
│
├── data/                                       # Fichiers CSV personnalisés de l’utilisateur
│   └── markets.csv                             # Données locales de l’utilisateur
│
├── design/                                     # Personnalisation de l’apparence
│   ├── inject_theme.py                         # Injecte dynamiquement un thème CSS dans l'app
│   ├── theme_colors.py                         # Palette de couleurs définie en Python
│   └── theme.css                               # Fichier CSS contenant le style complet à injecter
|
├── .devcontainer/
│   └── devcontainer.json
│
├── doc/                                        # Documentation du projet
│   ├── design.svg                              # Palette de couleurs de l'application
│   ├── folders-roles.png                       # @TODO : À supprimer si plus utilisé
│   └── structure.md                            # Ce fichier décrivant l’architecture du projet
|
├── pages/
│   ├── styles/
│   |   └── main.css
│   ├── Landing.py
│   ├── Login.py
│   ├── App.py
│   ├── admin.py
│   ├── super-admin.py
│   └── user.py
│
├── services/                                   # Couche "logique métier" – traitement des données
│   ├── cache/
│   │   └── geocoding_cache.py                  # Gère le chargement/sauvegarde du cache de géocodage
|   |
│   ├── mapping/
│   |   ├── client.py                           # Appels à l’API Nominatim
│   |   └── processor.py                        # Enrichissement de DataFrame avec coordonnées
|   |
│   ├── markets_analysis/
│   │   ├── load_markets_analysis.py            # Chargement des tendances de marché
│   │   └── save_markets_analysis.py            # Sauvegarde des données de marché
|   |
│   ├── offers/
│   │   ├── get_all_existing_markets.py # Récupération des marchés existants
│   │   ├── load_offers.py                      # Chargement des offres
│   │   └── save_offers.py                      # Sauvegarde d’une offre ou d’un contact
|   |
│   └── storage/
│       ├── append_to_market_file.py            # Ajout d’une ligne dans `markets.csv`
│       ├── supabase_storage_service.py         # Gère les échanges de fichiers avec Firebase Storage
│       ├── read_market_file.py                 # Lecture du fichier `markets.csv`
│       └── save_manager.py                     # Orchestration de sauvegardes (marché ou offres)
│
├── tabs/                                       # Pages principales de l’application
│   ├── compass.py                              # Logique + UI de l’onglet “Boussole”
│   ├── home.py                                 # Logique + UI de l’onglet “Accueil”
│   ├── market_analysis.py                      # Logique + UI de l’onglet “Analyse des marchés”
│   └── offer_dissection.py                     # Logique + UI de l’onglet “Dissection des offres”
│
└── utils/                                      # Utilitaires transverses
    ├── scripts/
    |   ├── csv.converter.py                    # Conversion d’anciens formats CSV vers le format unifié
    │   └── migrate_to_unified_markets.py       # Script de migration pour fusionner plusieurs fichiers de marché
    |
    ├── state/
    |   └── form_reset.py                       # Réinitialisation de formulaires dans session_state
    |
    ├── filters.py                              # Fonctions de filtrage et de sélection de marché
    ├── helpers.py                              # Fonctions utilitaires diverses
    ├── styling.py                              # Fonctions d’aide à la mise en forme (ex : colonnes colorées)
    └── validation.py                           # Vérifications de règles métier (unicité, etc.)

# Notes

- ✅ L’application supporte deux modes d’authentification : fake (dev) et Google OAuth (prod), définis dans `.streamlit/secrets.toml`.
- ✅ Les secrets sensibles (client_id, redirect_uri…) sont actuellement gérés dans `secrets.toml` (l'authentification) et dans `.env` (la persistance des données).
- 📂 Le dossier `services/` respecte une séparation stricte des responsabilités (auth / cache / storage / processing).
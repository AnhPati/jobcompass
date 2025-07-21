# =========================
# ⚠️ WARNINGS
# =========================

# --- Colonnes manquantes ---
WARNING_MISSING_COLUMN = "⚠️ La colonne {col} est manquante dans les données."

# --- Données indisponibles par catégorie ---
WARNING_NO_MAIN_SKILLS = "⚠️ Aucune compétence principale disponible pour ce marché."
WARNING_NO_SECONDARY_SKILLS = "⚠️ Aucune compétence secondaire disponible pour ce marché."
WARNING_NO_MAIN_TECH = "⚠️ Aucune technologie principale disponible pour ce marché."
WARNING_NO_SECONDARY_TECH = "⚠️ Aucune technologie secondaire disponible pour ce marché."
WARNING_NO_MARKET_ANALYSIS = "⚠️ Aucune analyse de marché n'est disponible."

# --- Validation ou saisie utilisateur ---
WARNING_MISSING_MARKET = "⚠️ Merci de spécifier un marché."
WARNING_MARKET_ALREADY_EXISTS = "⚠️ Une entrée pour ce marché à cette date existe déjà."
WARNING_TITLE_LINK_REQUIRED = "⚠️ Le titre et le lien de l'offre sont obligatoires."
WARNING_CONTACT_NAME_REQUIRED = "⚠️ Le nom du contact est requis."

# =========================
# ℹ️ INFO
# =========================

# --- Données absentes ou non disponibles ---
INFO_NO_TREND_DATA = "ℹ️ Aucune donnée de tendance disponible pour ce marché."
INFO_NO_RYTHM_DATA = "ℹ️ Aucune donnée sur le rythme de travail pour ce marché."
INFO_NO_SECTOR_DATA = "ℹ️ Aucune donnée sur le secteur de travail pour ce marché."
INFO_NO_MARKET_ANALYSIS_DATA = "ℹ️ Aucune donnée d'analyse de marché disponible."
INFO_NO_OFFERS_DATA = "ℹ️ Aucune offre enregistrée pour le moment."
INFO_NO_MARKET_FOR_OFFER_FORM = "ℹ️ Aucun marché n’a encore été suivi. Veuillez en ajouter un dans l’onglet 📈 Analyse des marchés."
INFO_NO_DATA_TO_DISPLAY = "ℹ️ Aucune donnée à afficher."
INFO_NO_MARKET_DATA_AVAILABLE = "ℹ️ Aucune donnée de type 'Marché' à afficher."
INFO_NO_COORDINATES_DATA = "ℹ️ Aucune donnée de localisation valide avec des coordonnées géographiques disponible pour ce marché sélectionné."
INFO_NO_NUMERIC_DATA = "ℹ️ Aucune donnée numérique valide disponible pour '{column_name}'."
INFO_NO_UNIQUE_VALUES = "ℹ️ Aucune valeur unique disponible pour l'exploration de '{column_name}'."
INFO_ONLY_ONE_NUMERIC_VALUE = "ℹ️ Une seule valeur disponible : {value}{unit}"

# --- Géocodage et carte ---
INFO_GEOCODING_IN_PROGRESS = "ℹ️ Géocodage de {count} localisation{s} non encore mises en cache ou manquantes. Cela peut prendre un certain temps..."
INFO_ALL_LOCATIONS_CACHED = "ℹ️ Toutes les localisations sont déjà géocodées ou mises en cache."
INFO_GEOCODING_PROGRESS = "ℹ️ Opération de géocodification en cours. Veuillez patienter..."
INFO_MAP_SUMMARY = (
    "ℹ️ Affichage de {n} localisation{s} unique{s} sur la carte pour le marché '{market_name}'. "
    "La couleur et la taille des points indiquent le nombre d'offres."
)

# =========================
# ✅ SUCCÈS
# =========================

SUCCESS_DATA_SAVED = "✅ Données ajoutées avec succès."
SUCCESS_OFFER_SAVED = "✅ Offre enregistrée avec succès !"
SUCCESS_FILE_IMPORTED = "✅ Fichier importé avec succès."
SUCCESS_GEOCODING_DONE = "✅ Géocodage terminé avec succès !"

# =========================
# ❌ ERREURS
# =========================

# --- Fichier ou colonnes invalides ---
ERROR_MISSING_TYPE_COLUMN = "❌ Colonne 'Type' introuvable. Le fichier a-t-il bien le bon séparateur ?"
ERROR_MISSING_LOCATION_COLUMN = "❌ La colonne '{column}' est manquante dans le DataFrame. Impossible de géocoder."
ERROR_FILE_PROCESSING = "❌ Erreur lors du traitement du fichier : {error}"

# --- Chargement / sauvegarde de données ---
ERROR_LOADING_MARKET_DATA = "❌ Erreur inattendue lors du chargement des données de marché : {error}"
ERROR_SAVING_MARKET_DATA = "❌ Erreur lors de la sauvegarde des données de marché : {error}"
ERROR_LOADING_OFFERS = "❌ Erreur inattendue lors du chargement des offres : {error}"
ERROR_SAVING_OFFERS = "❌ Erreur lors de la sauvegarde des offres : {error}"
ERROR_LOADING_MARKETS_FROM_OFFERS = "❌ Erreur lors de la récupération des marchés : {error}"
ERROR_INVALID_COLUMN_COUNT = "❌ Mauvais format : {detected} colonnes détectées (attendu : {expected}). Vérifiez le fichier."
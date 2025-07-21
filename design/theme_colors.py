# design/theme_colors.py

# 🎨 Jetons de design centralisés pour une utilisation côté Python (visualisation, markdown, mise en page)
# Ce dictionnaire reflète les variables CSS du thème, mais côté serveur dans Streamlit.

THEME = {
    # 🌈 Palette principale (Bleu)
    "primary": "#2f80ed",           # ! Couleur d'accent principale (boutons, liens, focus)
    "primary_hover": "#2073de",     # ! Variante au survol (hover) de la couleur principale

    # 🎨 Couleurs secondaires / d’alerte
    "danger": "#e53935",            # Erreurs, alertes, actions destructrices
    "warning": "#FBE1CE",           # ! Avertissements, messages d’attention
    "info": "#E0E9F5",              # ! Messages d’information ou bannières

    # 🖋 Couleurs de texte
    "text": "#3A1300",              # ! Couleur principale du texte (titres, paragraphes)
    "text_secondary": "#8B4100",    # ! Texte secondaire : sous-titres, aides, placeholders

    # 🧱 Couleurs de fond
    "background": "#F3F4F6",        # Fond global de la page
    "surface": "#ffffff",           # Fond des blocs, cartes, conteneurs
    "surface_alt": "#FDECE0",       # Variante légère pour alternance visuelle (ex. lignes de tableaux)

    # ➖ Bordures et séparateurs
    "border": "#F8C196",            # Bordure par défaut (inputs, cartes)
    "border_strong": "#6D9FE5",     # Bordure accentuée (titres, containers importants)

    # 🧾 Styles pour les tableaux de données (st.dataframe)
    "table_header_bg": "#B65A00",   # Fond de l’en-tête du tableau
    "table_header_text": "#ffffff", # Couleur du texte de l’en-tête
    "table_row_even": "#ECF0F6",    # Fond des lignes paires
    "table_row_odd": "#FDECE0",     # Fond des lignes impaires

    # 🔠 Typographie (police de secours)
    "font": "'Lato', sans-serif"    # À utiliser pour du markdown personnalisé si besoin
}

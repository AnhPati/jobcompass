# 📄 Product Requirements Document (PRD)

## 🧠 Contexte

Le projet a pour objectif de permettre à  toute personne visant un métier de l'**IT** de **s'appuyer sur sa prospection** afin d’**organiser son apprentissage** et **définir son positionnement** en se basant sur les **marchés** qu'elle suit. L’outil doit faciliter la visualisation des tendances du marché, permettre d’extraire des informations clés des offres, et suivre sa montée en compétence.

## 🎯 Objectif principal

Concevoir une application qui permet de :
- Suivre les marchés (plateformes, recruteurs, etc.)
- Récupérer et analyser les offres (scraping ou copier/coller)
- Extraire les besoins exprimés dans ces offres (techno, séniorité, rythme, etc.)
- Adapter et suivre son plan d’apprentissage en fonction de ces besoins

## 🧩 Fonctionnalités clés

### 1. Gestion des marchés suivis
- [x] Ajout/suppression d’un marché
- [x] Désactivation du formulaire si aucun marché n’est suivi

### 2. Ajout d’une offre
- [ ] Ajout via lien (scraping si possible)
- [x] Ajout via copier/coller manuel
- [x] Enregistrement des métadonnées : titre, entreprise, lien, marché, etc.

### 3. Extraction d'informations depuis l’offre
- [x] Intitulé du poste
- [x] TJM (ou fourchette salariale)
- [x] Date de publication (optionnelle)
- [x] Séniorité demandée
- [x] Techs principales et secondaires
- [x] Compétences principales et secondaires
- [x] Localisation
- [x] Rythme (remote/hybride/pré)  
- [x] Secteur
- [x] Type de client (ESN, final, agence…)
- [x] Contact (mail, LinkedIn, etc.)
- [x] Marché d’origine (plateforme)
- [x] Lien vers l’annonce

### 4. Visualisation des tendances
- [x] Graphiques des technos les plus demandées
- [x] Historique des offres
- [x] Fréquence des offres par marché
- [x] Diagrammes des secteurs et rythmes
- [x] Slider des TJMs et séniorités

### 5. Programme d’apprentissage personnalisé
- [ ] Génération d’un backlog de compétences à travailler
- [ ] Lien avec des ressources (par ex. docs, tutos)
- [ ] Suivi de progression
- [ ] Ajout manuel de compétences à travailler

## 👥 Utilisateur cible

Le projet s’adresse à toute personne évoluant (ou souhaitant évoluer) dans les métiers de la programmation et plus largement de l’IT, en particulier :

- Les développeurs en **reconversion** souhaitant structurer leur montée en compétence et cibler des postes réalistes
- Les développeurs **freelances** qui veulent aligner leur prospection avec les tendances du marché
- Les **juniors** en quête de repères pour se positionner et progresser efficacement
- Les **salariés** envisageant une évolution ou une transition vers d’autres missions

Ils ont en commun le besoin de :
- Comprendre les **attentes concrètes du marché**
- Organiser leur **apprentissage** de manière stratégique
- Suivre et centraliser leur **prospection ou leur veille**

## 🛠️ Contraintes techniques

- **Frontend** : Streamlit (avec utilisation du template [`streamlit-saas-starter`](https://github.com/antoineross/streamlit-saas-starter) pour la v1)
- **Backend** : 
  - Firebase (Firestore + Auth) ou Supabase selon faisabilité avec l’environnement Streamlit
  - À noter : Firebase Auth **ne fonctionne pas nativement** avec Streamlit Cloud (pas de redirection OAuth via Google depuis un frontend hébergé sur Streamlit Cloud)
  > 📌 Remarque : Supabase est privilégié si l’auth et la base relationnelle doivent coexister nativement avec Streamlit Cloud.
- **Authentification** : via Google uniquement, gérée côté backend
- **Hébergement** :
  - **v1** hébergée sur Streamlit Cloud
  - Possibilité d’évoluer vers un hébergement externe (Railway, Render, etc.) pour plus de contrôle
- **Stockage des données** : persistance des données utilisateurs obligatoire (offres, extractions, apprentissage, etc.)
- **Pas d’outils externes** (Zapier, Make...) : toute l’automatisation doit se faire en natif (Python / Firebase Functions ou équivalent)
- **Évolutions futures** : possibilité de migrer vers une stack hybride :
  - Frontend en React (avec composants Streamlit wrappés ou remplacés)
  - Backend Python conservé pour le scraping, l’extraction, et la logique métier
- **Encodage** : UTF-8 requis (notamment pour l’utilisation d’emojis dans les fichiers CSS)

## 📦 Données stockées

### 📌 État actuel
- `users`: identifiant + email (authentification via Google)
- `csv_data`: fichier CSV structuré stocké pour chaque utilisateur, contenant les données consolidées sur les offres, marchés suivis et actions de prospection (source principale pour l’analyse et la suggestion)

### 🔮 Évolutions prévues (modèle relationnel Supabase/PostgreSQL)
- `users`: profil enrichi (email, objectifs, séniorité, stack cible, etc.)
- `offers`: offres structurées et analysées automatiquement à partir du CSV ou d’un scraping
- `contacts`: données issues de contacts manuels (recruteurs, leads), avec schéma spécifique
- `skills`: backlog de compétences à acquérir (issues des offres ou ajoutées manuellement)
- `markets`: canaux suivis (LinkedIn, Freework, etc.)
- `tracking`: historique des actions de prospection et des apprentissages réalisés

🎯 L’objectif est de passer d’un simple fichier CSV à une base relationnelle, permettant :
- l’analyse automatique et le croisement des données
- des suggestions personnalisées (offres similaires, parcours d’apprentissage)
- une meilleure gestion des utilisateurs et de leurs parcours

## ✅ Critères d’acceptation

- Interface fluide et responsive
- Application utilisable dès les premières offres enregistrées
- Extraction automatique ou semi-automatique des infos clés d’une offre
- Visualisation simple des tendances (graphes ou listes)
- Backlog de compétences personnalisées à jour

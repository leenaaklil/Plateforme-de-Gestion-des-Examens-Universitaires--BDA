📚 Plateforme d'Optimisation des Emplois du Temps d'Examens Universitaires
https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white
https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white
https://img.shields.io/badge/License-MIT-blue.svg

🌟 Aperçu du Projet
Une plateforme complète pour optimiser automatiquement les emplois du temps d'examens universitaires. Conçue pour gérer 13,000+ étudiants, 200+ formations, et générer des plannings optimisés en moins de 45 secondes.

🎯 Contexte et Problématique
Dans une faculté de plus de 13,000 étudiants répartis sur 7 départements et 200+ offres de formation (6-9 modules par formation), l'élaboration manuelle des emplois du temps génère fréquemment des conflits : surcharge des amphis, salles limitées, chevauchements étudiants/professeurs, contraintes d'équipements.

✨ Fonctionnalités Principales
✅ Génération automatique d'emplois du temps optimisés

✅ Détection intelligente des conflits en temps réel

✅ Optimisation basée sur algorithmes génétiques

✅ Tableaux de bord interactifs multi-rôles

✅ Validation de toutes les contraintes académiques

✅ Export des plannings (PDF, CSV, Excel)

✅ Interface web moderne et intuitive

📁 Structure du Projet
text
📦 projet-optimisation-examens/
├── 📂 app/
│   ├── main.py                    # Application Streamlit principale
│   ├── config.py                  # Configuration de l'application
│   ├── database.py                # Gestionnaire de base de données
│   └── 📂 services/               # Services métier
│       ├── generator.py           # Générateur d'emploi du temps
│       ├── optimizer.py           # Optimisation algorithmique
│       └── validator.py           # Validation des contraintes
├── 📂 backend/
│   ├── db_connection.py           # Connexion MySQL/SQLite
│   ├── schedule_generator.py      # Générateur de planning
│   └── constraint_validator.py    # Validateur de contraintes
├── 📂 database/
│   ├── 01_setup_database.sql      # Création de la base
│   ├── 02_create_tables.sql       # Tables principales
│   ├── 03_insert_data.sql         # Données de test (13k étudiants)
│   ├── 04_stored_procedures.sql   # Procédures stockées
│   └── 05_create_views.sql        # Vues pour reporting
├── 📂 pages/                      # Pages Streamlit
│   ├── 0_🏠_Accueil.py
│   ├── 1_📊_Dashboard.py
│   ├── 2_📅_Générer_EDT.py
│   ├── 3_👨‍🎓_Étudiants.py
│   ├── 4_👨‍🏫_Professeurs.py
│   └── 5_🏢_Administration.py
├── 📂 assets/                     # Ressources
├── 📂 scripts/                    # Scripts utilitaires
├── requirements.txt               # Dépendances Python
├── .streamlit/
│   └── config.toml               # Configuration Streamlit
├── README.md                     # Ce fichier
└── LICENSE                       # Licence MIT
🚀 Installation Rapide
Prérequis
Python 3.9+

XAMPP (pour MySQL local) ou SQLite (pour test simple)

Git

Option 1 : Installation avec XAMPP (Recommandé)
Étape 1 : Installer XAMPP
Téléchargez XAMPP depuis apachefriends.org

Installez-le à C:\xampp\ (Windows) ou /Applications/XAMPP/ (Mac)

Démarrez Apache et MySQL dans le panneau de contrôle

Étape 2 : Configurer la base de données
Ouvrez phpMyAdmin

Créez une nouvelle base : planning_examens_db

Cliquez sur "SQL" et exécutez les fichiers dans cet ordre :

database/01_setup_database.sql

database/02_create_tables.sql

database/03_insert_data.sql (données de test)

database/04_stored_procedures.sql

database/05_create_views.sql

Étape 3 : Configurer l'application
bash
# 1. Cloner le projet
git clone https://github.com/votre-repo/planning-examens.git
cd planning-examens

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
streamlit run app/main.py
Option 2 : Installation avec SQLite (Plus simple)
Cloner le projet

Installer les dépendances :

bash
pip install streamlit pandas plotly
Lancer l'application :

bash
streamlit run app/main.py
L'application créera automatiquement une base SQLite dans database/exams.db

🎮 Utilisation de l'Application
Accès
URL locale : http://localhost:8501

Identifiants de démonstration :

Administrateur : admin / admin123

Étudiant : ETU000001 / etudiant

Professeur : PROF001 / professeur

Fonctionnalités par Rôle
👨‍💼 Administrateur / Vice-doyen
Vue stratégique globale

Occupation des amphis et salles

Taux de conflits par département

Validation finale des EDT

KPIs académiques (heures profs, taux d'utilisation...)

📋 Administrateur Examens
Génération automatique d'EDT

Détection et résolution des conflits

Optimisation des ressources

Gestion des contraintes

🎓 Étudiants
Consultation du planning personnel

Filtrage par département/formation

Export du planning (CSV)

Notifications des examens

👨‍🏫 Professeurs
Consultation des surveillances

Statistiques personnelles

Disponibilités

Planning des examens

🗄️ Structure de la Base de Données
Tables Principales
departements (7 départements)

formations (35 formations, 5 par département)

etudiants (13,000+ étudiants)

modules (6-9 par formation, ~200 modules)

salles (50+ salles avec capacités variées)

professeurs (100+ professeurs)

inscriptions (130,000+ inscriptions)

examens (planning généré)

surveillances (affectation des professeurs)

Contraintes Implémentées
Étudiants : Maximum 1 examen par jour

Professeurs : Maximum 3 examens par jour

Salles : Respect de la capacité réelle

Priorités : Examens du département priorisés

Équilibre : Tous les enseignants ont approximativement le même nombre de surveillances

Temporalité : 30 minutes minimum entre deux examens dans la même salle

Disponibilité : Pas d'examens le week-end

🔧 Configuration Avancée
Variables d'Environnement
Créez un fichier .env à la racine :

env
# Pour MySQL local avec XAMPP
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=planning_examens_db

# Pour Streamlit Cloud (secrets)
DATABASE_URL=mysql://user:pass@host/db
Configuration Streamlit
Éditez .streamlit/config.toml :

toml
[theme]
primaryColor = "#1E3A8A"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
address = "0.0.0.0"
enableCORS = false
🚀 Déploiement en Production
Option 1 : Streamlit Cloud (Gratuit)
Poussez votre code sur GitHub

Allez sur share.streamlit.io

Connectez votre GitHub

Configurez les secrets :

toml
# Dans Streamlit Cloud Secrets
DATABASE_URL = "mysql://user:pass@host/db"
Option 2 : Google Cloud Platform
bash
# Utilisez le script de déploiement
chmod +x scripts/deploy_gcp.sh
./scripts/deploy_gcp.sh
Option 3 : Docker
bash
# Construire et lancer
docker-compose up -d
# Accéder à http://localhost:8501
📊 Algorithmes d'Optimisation
Algorithme Génétique
Population : 100 solutions candidates

Sélection : Tournoi

Croisement : Point unique

Mutation : 10% de probabilité

Fitness : Basée sur les violations de contraintes

Heuristiques Implémentées
First-Fit Decreasing pour l'allocation des salles

Backtracking pour la résolution de contraintes

Hill Climbing pour l'optimisation locale

Constraint Satisfaction Problem (CSP)

🧪 Tests et Validation
Tests de Performance
bash
# Lancer les tests de performance
python tests/test_performance.py

# Résultats attendus :
# ✅ Génération EDT : < 45 secondes
# ✅ Conflits étudiants : 0%
# ✅ Conflits professeurs : < 5%
# ✅ Utilisation salles : > 70%
Validation des Contraintes
python
from backend.constraint_validator import validator

# Vérifier toutes les contraintes
report = validator.validate_all_constraints()
print(f"Score de conformité: {report['compliance_score']}%")
📈 Statistiques du Projet
Métrique	Valeur
Étudiants	13,000+
Professeurs	100+
Formations	35
Modules	200+
Salles	50+
Inscriptions	130,000+
Temps de génération	< 45s
Taux de réussite	> 95%
🎥 Pour la Vidéo de Présentation
Structure Recommandée (5-10 minutes)
text
0:00-0:30  - Introduction et contexte
0:30-1:30  - Installation et configuration
1:30-2:30  - Démonstration : Génération automatique
2:30-3:30  - Vue administrateur et statistiques
3:30-4:30  - Vue étudiant/professeur
4:30-5:30  - Optimisation et résolution conflits
5:30-6:00  - Déploiement en ligne
6:00-7:00  - Conclusion et avantages
Points à Mettre en Avant
Rapidité : Génération en < 45 secondes

Échelle : Support de 13,000+ étudiants

Intelligence : Algorithmes d'optimisation

Simplicité : Interface intuitive

Robustesse : Validation complète des contraintes

🤝 Contribution
Fork le projet

Créez une branche : git checkout -b feature/ma-fonctionnalite

Commitez : git commit -m 'Ajout de ma fonctionnalité'

Poussez : git push origin feature/ma-fonctionnalite

Ouvrez une Pull Request

Guide de Style
Nommage : anglais pour le code, français pour les commentaires

Documentation : docstrings pour toutes les fonctions

Tests : unitaires pour les algorithmes critiques

Commits : messages en français, format conventionnel

📝 Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

🙏 Remerciements
Streamlit pour l'infrastructure d'application web

MySQL/PostgreSQL pour la gestion des données

Plotly pour les visualisations interactives

La communauté open-source pour les nombreuses bibliothèques utilisées

📞 Support
Pour toute question ou problème :

Consultez les Issues GitHub

Contactez l'équipe : contact@planning-examens.fr

Rejoignez notre Discord : [lien-invitation]

<div align="center"> <p>Développé avec ❤️ pour simplifier la vie universitaire</p> <p>⭐ Star ce projet si vous le trouvez utile !</p> </div>
🔗 Liens Utiles
📚 Documentation Complète

🐛 Signaler un Bug

💡 Suggestions de Fonctionnalités

🎥 Vidéo de Démonstration

🌐 Application en Ligne

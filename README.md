# 📚 Plateforme d'Optimisation des Emplois du Temps d'Examens Universitaires

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

<div>
  Si vous rencontrez un problème avec le lien de la plateforme, veuillez nous contacter à l'adresse aklillyna2003@gmail.com. En effet, notre période d'hébergement est limitée, vous pourriez donc rencontrer des difficultés.
</div>
## 🌟 Aperçu du Projet

<div align="center">
  
  **Optimisez automatiquement les emplois du temps d'examens pour 13,000+ étudiants**
  
  [🚀 Voir la Démo en Ligne](https://youtu.be/nuAYw41ClV0) | [📖 Documentation](#) | [🐛 Signaler un Bug](https://github.com/leenaaklil/Plateforme-de-Gestion-des-Examens-Universitaires--BDA/issues)
  
</div>

---

## 📋 Table des Matières
- [✨ Fonctionnalités](#-fonctionnalités)
- [🚀 Installation Rapide](#-installation-rapide)

## ✨ Fonctionnalités

### 🎯 Génération & Optimisation
| Fonctionnalité | Description | Statut |
|---------------|-------------|--------|
| ✅ **Génération automatique** | Crée des EDT optimisés en < 45 secondes | Production |
| ✅ **Détection de conflits** | Identifie les conflits étudiants/professeurs | Production |
| ✅ **Algorithmes d'optimisation** | Génétique + CSP pour une optimisation maximale | Production |
| ✅ **Validation contraintes** | Vérifie toutes les contraintes académiques | Production |


## 🚀 Installation Rapide

### Prérequis
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)

### Installation Complète

```bash
# 1. Cloner le dépôt
git clone https://github.com/leenaaklil/Plateforme-de-Gestion-des-Examens-Universitaires-BDA.git
cd Plateforme-de-Gestion-des-Examens-Universitaires-BDA

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer la base de données (avec XAMPP)
# - Démarrez XAMPP/WAMP (Apache + MySQL)
# - Ouvrez http://localhost/phpmyadmin
# - Créer une base de données : edt_examens
# 1ère option :
# - Importez le fichiers SQL :
#   database/edt_examens.sql
# 2ème option :
# -  Importez le fichier SQL :
#   database/schema.sql
#   run fake_data_generator : python fake_data_generator.py                                                   

# 4. Lancer l'application
python -m streamlit run app.py
 















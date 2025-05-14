# hackathon_cjp
Technologies utilisées dans le projet SignalGuinée
Stack technique
Backend

Django 5.0.2 (Framework Python)
Python 3.12.2
SQLite (Base de données par défaut)
Frontend

HTML5
CSS3
Bootstrap 5.3.0
JavaScript
Font Awesome 6.0.0
Cartographie

Leaflet.js
Leaflet MarkerCluster
Autres bibliothèques

Chart.js (pour les graphiques)
DataTables (pour les tableaux interactifs)
jQuery 3.6.0
Guide de démarrage
Prérequis
Python 3.12+ installé
Git installé
Un éditeur de code (VS Code recommandé)
Étapes d'installation
Cloner le projet
git clone <url-du-repo>
cd signalisation
Créer un environnement virtuel
python -m venv venv
Activer l'environnement virtuel
# Pour Windows
venv\Scripts\activate

# Pour Linux/Mac
source venv/bin/activate
Installer les dépendances
pip install -r requierment_j.txt
Configurer les variables d'environnement
Créer un fichier .env à la racine du projet
SECRET_KEY=votre-cle-secrete
SECRET_KEY = 'django-insecure-f!+lhv7slam-21&0va=j!ovhzx_vp2y7_wq!9+m6^zi4w3+wg+'
DEBUG=True
Appliquer les migrations
python manage.py migrate
Créer un super utilisateur
python manage.py createsuperuser
Lancer le serveur de développement
L'application sera accessible à l'adresse : http://127.0.0.1:8000/

Structure du projet
Fonctionnalités principales
Inscription/Connexion des utilisateurs
Création et suivi des signalements
Tableau de bord administrateur
Visualisation cartographique
Gestion des administrateurs
Statistiques et rapports
Notes importantes
Assurez-vous que Python et pip sont bien installés (python --version)
En cas de problème avec les dépendances : pip install --upgrade pip
Pour les problèmes de migration : python [manage.py](http://_vscodecontentref_/0) makemigrations
Vérifiez les permissions des dossiers media/ et static/

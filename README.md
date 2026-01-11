# NYC Crime Intelligence Dashboard 🏙️

Bienvenue dans mon **Système Avancé de Prédictions de Criminalité**. J'ai conçu ce projet pour transformer les données historiques brutes de la ville de New York en un tableau de bord interactif et intelligent. En utilisant le Machine Learning, cet outil permet de visualiser et de prédire les risques potentiels basés sur des facteurs spatiaux, temporels et démographiques.

## 🚀 La Vision
Mon objectif était de créer plus qu'un simple tableau de données. Je voulais construire une **interface premium au style "glassmorphic"** qui ressemble à un centre de commandement moderne, permettant à chacun d'évaluer les niveaux de sécurité locale en un clic.

---

## 🏗️ Comment je l'ai construit

### 1. Le Cerveau (Backend)
J'ai choisi **FastAPI** pour sa haute performance et sa simplicité.
- **Intégration du Modèle** : J'ai intégré un modèle **LightGBM** entraîné sur les données historiques de la NYPD de 2006 à 2021.
- **Pipeline de Données** : J'ai développé un script de traitement personnalisé dans `api/main.py` qui reçoit les entrées utilisateur (lieu, heure, profil) et les convertit en un vecteur de 36 caractéristiques pour le modèle.
- **Intelligence** : Le système ne se contente pas de prédire une catégorie ; il calcule un **Score de Confiance** et associe les sorties du modèle à des sous-catégories compréhensibles (Burglary, Assault, Drugs, etc.).

### 2. L'Expérience (Frontend)
J'ai évité les frameworks lourds pour garder un tableau de bord rapide et fluide.
- **Interface Moderne** : Construite avec **HTML5, Vanilla CSS3**, et **JavaScript**. J'ai utilisé des effets de flou (Glassmorphism), des animations fluides et une typographie soignée.
- **Cartographie Interactive** : J'ai intégré **Leaflet.js** avec des fonds de carte en mode sombre. Les utilisateurs peuvent cliquer n'importe où dans les 5 boroughs pour capturer instantanément les coordonnées.
- **Design Réactif** : La barre latérale gère les entrées complexes, tandis que la zone principale se concentre sur la carte et les cartes de résultats.

---

## 🛠️ Fonctionnalités Clés
- **Sélection sur Carte en Temps Réel** : Cliquez pour définir les coordonnées d'analyse.
- **Profilage Démographique** : Analysez les risques selon l'âge, le genre et l'ethnie.
- **Analyse Temporelle** : Filtrez par date et heure pour voir l'évolution des schémas criminels.
- **Score de Confiance** : Des barres de progression dynamiques indiquent la certitude de l'IA.

---

## 💻 Guide d'Installation

Pour lancer ce tableau de bord localement sur votre machine :

### 1. Configuration de l'Environnement
Créez un environnement virtuel et installez les bibliothèques requises :
```bash
# Créer l'environnement
python -m venv venv

# Activer (Windows)
.\venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Lancement de l'Application
Lancez le serveur FastAPI. Il s'occupe à la fois des points d'accès API et de servir les fichiers statiques du frontend :
```bash
python api/main.py
```
Ouvrez votre navigateur et allez sur `http://localhost:8000`.

---

## 📈 Prochaines Étapes
Je travaille actuellement sur l'extension du tableau de bord pour inclure :
- **Analyse Complète des Risques** : Afficher la probabilité de chaque catégorie au lieu de seulement la prédiction principale.
- **Comparaison Historique** : Montrer comment la prédiction actuelle se compare aux mêmes jours des années précédentes.

---

*Ce projet a été développé avec une attention particulière portée à la combinaison de la science des données et d'un design web de haut niveau.*
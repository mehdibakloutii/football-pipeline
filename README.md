# ⚽ Football Data Pipeline

Pipeline de données end-to-end sur les données de football.

## 🏗️ Architecture

API Football → Python → PostgreSQL → dbt → Dashboard

## 🛠️ Technologies utilisées

- Python 3.13
- PostgreSQL 18
- dbt (coming soon)
- Airflow (coming soon)

## 📦 Installation

1. Cloner le repo
git clone https://github.com/ton_username/football-pipeline.git

2. Créer l'environnement virtuel
python -m venv venv
venv\Scripts\activate

3. Installer les dépendances
pip install -r requirements.txt

4. Configurer le fichier .env
cp .env.example .env

5. Lancer le pipeline
python main.py

## 📊 Données

- 13 compétitions européennes et mondiales
- 380 matchs de Premier League
- Mise à jour manuelle via main.py
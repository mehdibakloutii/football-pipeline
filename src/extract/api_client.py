import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.football-data.org/v4"

headers = {
    "X-Auth-Token": API_KEY
}

def get_competitions():
    """Récupère la liste des compétitions disponibles"""
    url = f"{BASE_URL}/competitions"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ {len(data['competitions'])} compétitions récupérées !")
        return data['competitions']
    else:
        print(f"❌ Erreur : {response.status_code}")
        return None

def get_matches(competition_code="PL", matchday=1):
    """Récupère les matchs d'une compétition (PL = Premier League)"""
    url = f"{BASE_URL}/competitions/{competition_code}/matches"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ {len(data['matches'])} matchs récupérés !")
        return data['matches']
    else:
        print(f"❌ Erreur : {response.status_code}")
        return None

if __name__ == "__main__":
    print("🔍 Test de connexion à l'API...")
    competitions = get_competitions()
    
    if competitions:
        print("\n📋 Premières compétitions disponibles :")
        for comp in competitions[:5]:
            print(f"  - {comp['name']} ({comp['code']})")
    
    print("\n⚽ Récupération des matchs de Premier League...")
    matches = get_matches("PL")
    
    if matches:
        print("\n📋 Premiers matchs :")
        for match in matches[:3]:
            home = match['homeTeam']['name']
            away = match['awayTeam']['name']
            date = match['utcDate'][:10]
            print(f"  - {home} vs {away} ({date})")
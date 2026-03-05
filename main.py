from src.extract.api_client import get_competitions, get_matches
from src.load.db_loader import insert_competitions, insert_matches

print("🚀 Démarrage du pipeline football...")

print("\n📡 Extraction des données depuis l'API...")
competitions = get_competitions()
matches = get_matches("PL")

print("\n💾 Chargement dans PostgreSQL...")
insert_competitions(competitions)
insert_matches(matches, "PL")

print("\n✅ Pipeline terminé avec succès !")
print(f"   - {len(competitions)} compétitions chargées")
print(f"   - {len(matches)} matchs chargées")
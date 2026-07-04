"""
Module de recommandation des meilleurs horaires de publication.
Basé sur des données générales d'engagement TikTok par jour/heure.
"""

MEILLEURS_CRENEAUX = {
    "lundi": ["06:00", "10:00", "22:00"],
    "mardi": ["02:00", "04:00", "09:00"],
    "mercredi": ["07:00", "08:00", "23:00"],
    "jeudi": ["09:00", "12:00", "19:00"],
    "vendredi": ["05:00", "13:00", "15:00"],
    "samedi": ["11:00", "19:00", "20:00"],
    "dimanche": ["07:00", "08:00", "16:00"],
}

def obtenir_creneaux(jour: str) -> list:
    """Retourne les créneaux horaires recommandés pour un jour donné."""
    jour = jour.lower().strip()
    return MEILLEURS_CRENEAUX.get(jour, ["Jour non reconnu"])


if __name__ == "__main__":
    jour = input("Entrez le jour de publication (lundi, mardi, ...) : ")
    creneaux = obtenir_creneaux(jour)
    print(f"\nMeilleurs créneaux pour {jour} :")
    for c in creneaux:
        print(f"  {c}")

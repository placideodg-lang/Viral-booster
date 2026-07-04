"""
Amplificateur Viral - Outil d'aide à la croissance TikTok
Point d'entrée principal du programme.
"""

from hashtags import suggerer_hashtags
from scheduler import obtenir_creneaux


def menu():
    print("=" * 40)
    print("  AMPLIFICATEUR VIRAL - TikTok Booster")
    print("=" * 40)
    print("1. Suggestions de hashtags")
    print("2. Meilleurs horaires de publication")
    print("3. Quitter")

    choix = input("\nVotre choix : ").strip()

    if choix == "1":
        niche = input("Votre niche : ")
        for tag in suggerer_hashtags(niche):
            print(f"  {tag}")
    elif choix == "2":
        jour = input("Jour de publication : ")
        for c in obtenir_creneaux(jour):
            print(f"  {c}")
    elif choix == "3":
        print("À bientôt !")
        return
    else:
        print("Choix invalide.")

    menu()


if __name__ == "__main__":
    menu()

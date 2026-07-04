"""
Module de suggestion de hashtags pertinents par niche.
Rotation automatique hebdomadaire pour varier les suggestions.
"""

import datetime
import random

# Grande banque de hashtags par niche (on peut en ajouter autant qu'on veut)
BANQUE_HASHTAGS = {
    "humour": ["#humour", "#fun", "#comedie", "#rire", "#sketch", "#drole",
               "#humournoir", "#blague", "#lol", "#mdr", "#tiktokhumour"],
    "lifestyle": ["#lifestyle", "#dailyvibe", "#motivation", "#routine",
                  "#inspiration", "#viequotidienne", "#bienetre", "#positivevibes"],
    "education": ["#apprendre", "#education", "#astuce", "#savoir",
                  "#connaissance", "#tips", "#formation", "#culture"],
    "gaming": ["#gaming", "#jeuxvideo", "#gamer", "#gameplay",
               "#esport", "#streamer", "#jeuxmobile", "#tiktokgaming"],
    "business": ["#entrepreneur", "#business", "#startup", "#succes",
                 "#motivation", "#argent", "#investissement", "#businessplan"],
}


def numero_semaine_actuelle() -> int:
    """Retourne le numéro de la semaine dans l'année (change chaque semaine)."""
    return datetime.date.today().isocalendar()[1]


def suggerer_hashtags(niche: str, nombre: int = 5) -> list:
    """
    Retourne une sélection de hashtags qui change chaque semaine,
    en piochant dans la banque complète pour cette niche.
    """
    niche = niche.lower().strip()
    banque = BANQUE_HASHTAGS.get(niche, ["#tiktok", "#viral", "#fyp"])

    # La graine change chaque semaine → sélection différente automatiquement
    graine = numero_semaine_actuelle() + hash(niche) % 1000
    rng = random.Random(graine)

    nombre = min(nombre, len(banque))
    return rng.sample(banque, nombre)


if __name__ == "__main__":
    niche = input("Entrez votre niche (humour, lifestyle, education, gaming, business) : ")
    resultats = suggerer_hashtags(niche)
    print(f"\nHashtags suggérés pour '{niche}' cette semaine :")
    for tag in resultats:
        print(f"  {tag}")

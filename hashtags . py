"""
Module de suggestion de hashtags pertinents par niche.
"""

HASHTAGS_PAR_NICHE = {
    "humour": ["#humour", "#fun", "#comedie", "#rire", "#sketch"],
    "lifestyle": ["#lifestyle", "#dailyvibe", "#motivation", "#routine"],
    "education": ["#apprendre", "#education", "#astuce", "#savoir"],
    "gaming": ["#gaming", "#jeuxvideo", "#gamer", "#gameplay"],
    "business": ["#entrepreneur", "#business", "#startup", "#succes"],
}

def suggerer_hashtags(niche: str) -> list:
    """Retourne une liste de hashtags suggérés pour une niche donnée."""
    niche = niche.lower().strip()
    return HASHTAGS_PAR_NICHE.get(niche, ["#tiktok", "#viral", "#fyp"])


if __name__ == "__main__":
    niche = input("Entrez votre niche (humour, lifestyle, education, gaming, business) : ")
    resultats = suggerer_hashtags(niche)
    print(f"\nHashtags suggérés pour '{niche}' :")
    for tag in resultats:
        print(f"  {tag}")

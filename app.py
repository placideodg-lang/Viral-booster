import streamlit as st
from hashtags import suggerer_hashtags
from scheduler import obtenir_creneaux

st.set_page_config(page_title="Amplificateur Viral - TikTok Booster", page_icon="🚀")

# Liste des codes d'accès valides (ajoute-en un nouveau pour chaque client)
CODES_VALIDES = {
    "KABO2026",
    "VIRAL100",
}

# Initialisation de l'état de session
if "acces_premium" not in st.session_state:
    st.session_state.acces_premium = False

st.title("🚀 Amplificateur Viral")
st.subheader("Outil d'aide à la croissance TikTok")

st.markdown("---")

# Zone de déverrouillage
if not st.session_state.acces_premium:
    st.info("🔒 Version gratuite limitée. Entrez votre code d'accès premium pour débloquer toutes les niches.")
    code_saisi = st.text_input("Code d'accès premium", type="password")
    if st.button("Déverrouiller"):
        if code_saisi in CODES_VALIDES:
            st.session_state.acces_premium = True
            st.success("Accès premium débloqué !")
            st.rerun()
        else:
            st.error("Code invalide. Contactez Kabo Média pour obtenir un accès.")

st.markdown("---")

onglet1, onglet2 = st.tabs(["📊 Hashtags", "⏰ Horaires de publication"])

niches_gratuites = ["humour"]
niches_toutes = ["humour", "lifestyle", "education", "gaming", "business"]

with onglet1:
    st.write("Découvrez les meilleurs hashtags pour votre niche.")
    options_niches = niches_toutes if st.session_state.acces_premium else niches_gratuites
    niche = st.selectbox("Choisissez votre niche :", options_niches)
    if not st.session_state.acces_premium:
        st.caption("🔒 Débloquez toutes les niches avec un code premium.")
    if st.button("Obtenir les hashtags", key="hashtags"):
        resultats = suggerer_hashtags(niche)
        st.success(f"Hashtags suggérés pour **{niche}** :")
        for tag in resultats:
            st.write(f"- {tag}")

with onglet2:
    if st.session_state.acces_premium:
        st.write("Trouvez les meilleurs créneaux pour publier.")
        jour = st.selectbox(
            "Choisissez le jour :",
            ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
        )
        if st.button("Obtenir les créneaux", key="scheduler"):
            creneaux = obtenir_creneaux(jour)
            st.success(f"Meilleurs créneaux pour **{jour}** :")
            for c in creneaux:
                st.write(f"- {c}")
    else:
        st.warning("🔒 Fonctionnalité réservée aux utilisateurs premium. Entrez votre code d'accès ci-dessus.")

st.markdown("---")
st.caption("Cet outil ne génère aucune vue, like ou interaction artificielle. Il aide uniquement à optimiser votre stratégie de contenu.")

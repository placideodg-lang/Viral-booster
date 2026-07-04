import streamlit as st
from hashtags import suggerer_hashtags
from scheduler import obtenir_creneaux

st.set_page_config(page_title="Amplificateur Viral - TikTok Booster", page_icon="🚀")

st.title("🚀 Amplificateur Viral")
st.subheader("Outil d'aide à la croissance TikTok")

st.markdown("---")

onglet1, onglet2 = st.tabs(["📊 Hashtags", "⏰ Horaires de publication"])

with onglet1:
    st.write("Découvrez les meilleurs hashtags pour votre niche.")
    niche = st.selectbox(
        "Choisissez votre niche :",
        ["humour", "lifestyle", "education", "gaming", "business"]
    )
    if st.button("Obtenir les hashtags", key="hashtags"):
        resultats = suggerer_hashtags(niche)
        st.success(f"Hashtags suggérés pour **{niche}** :")
        for tag in resultats:
            st.write(f"- {tag}")

with onglet2:
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

st.markdown("---")
st.caption("Cet outil ne génère aucune vue, like ou interaction artificielle. Il aide uniquement à optimiser votre stratégie de contenu.")

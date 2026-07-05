import streamlit as st
from hashtags import suggerer_hashtags
from scheduler import obtenir_creneaux
from supabase import create_client
from datetime import datetime, timezone

st.set_page_config(page_title="Amplificateur Viral - TikTok Booster", page_icon="🚀", layout="centered")
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .stButton button {
        width: 100%;
        height: 3em;
        font-size: 1.1em;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1em;
        padding: 0.5em;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# Connexion a Supabase (cles stockees dans .streamlit/secrets.toml)
# ============================================
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_ANON_KEY"])

LIMITE_GRATUITE = 3


def obtenir_profil(user_id):
    """Recupere le profil utilisateur depuis Supabase."""
    reponse = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
    return reponse.data


def verifier_et_reinitialiser_compteur(profil):
    """Reinitialise le compteur mensuel si un mois s'est ecoule."""
    dernier_reset = datetime.fromisoformat(profil["date_dernier_reset"].replace("Z", "+00:00").split(".")[0] + "+00:00")
    maintenant = datetime.now(timezone.utc)

    if maintenant.month != dernier_reset.month or maintenant.year != dernier_reset.year:
        supabase.table("profiles").update({
            "analyses_utilisees_ce_mois": 0,
            "date_dernier_reset": maintenant.isoformat(),
        }).eq("id", profil["id"]).execute()
        profil["analyses_utilisees_ce_mois"] = 0

    return profil


def incrementer_utilisation(user_id, valeur_actuelle):
    """Incremente le compteur d'analyses utilisees."""
    supabase.table("profiles").update({
        "analyses_utilisees_ce_mois": valeur_actuelle + 1
    }).eq("id", user_id).execute()


# ============================================
# Initialisation de l'etat de session
# ============================================
if "utilisateur" not in st.session_state:
    st.session_state.utilisateur = None
if "profil" not in st.session_state:
    st.session_state.profil = None

st.title("🚀 Amplificateur Viral")
st.subheader("Outil d'aide à la croissance TikTok")

# ============================================
# Connexion / Inscription
# ============================================
if st.session_state.utilisateur is None:
    st.markdown("---")
    onglet_connexion, onglet_inscription = st.tabs(["Se connecter", "Créer un compte"])

    with onglet_connexion:
        email = st.text_input("Email", key="email_connexion")
        mot_de_passe = st.text_input("Mot de passe", type="password", key="mdp_connexion")
        if st.button("Se connecter"):
            try:
                resultat = supabase.auth.sign_in_with_password({"email": email, "password": mot_de_passe})
                st.session_state.utilisateur = resultat.user
                st.session_state.profil = obtenir_profil(resultat.user.id)
                st.rerun()
            except Exception as e:
                st.error("Email ou mot de passe incorrect.")

    with onglet_inscription:
        nom = st.text_input("Nom complet", key="nom_inscription")
        email_i = st.text_input("Email", key="email_inscription")
        mdp_i = st.text_input("Mot de passe", type="password", key="mdp_inscription")
        if st.button("Créer mon compte"):
            try:
                resultat = supabase.auth.sign_up({
                    "email": email_i,
                    "password": mdp_i,
                    "options": {"data": {"nom_complet": nom}}
                })
                st.success("Compte créé ! Tu peux maintenant te connecter.")
            except Exception as e:
                st.error(f"Erreur lors de la création du compte : {e}")

    st.stop()

# ============================================
# Utilisateur connecte : rafraichir le profil et le compteur
# ============================================
profil = verifier_et_reinitialiser_compteur(st.session_state.profil)
est_premium = profil["statut_abonnement"] == "premium"
utilisees = profil["analyses_utilisees_ce_mois"]
restantes = max(0, LIMITE_GRATUITE - utilisees)

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"Connecté en tant que **{profil.get('nom_complet') or profil['email']}**")
with col2:
    if st.button("Déconnexion"):
        supabase.auth.sign_out()
        st.session_state.utilisateur = None
        st.session_state.profil = None
        st.rerun()

if est_premium:
    st.success("✨ Compte Premium — analyses illimitées")
else:
    st.info(f"🔓 Compte gratuit — {restantes}/{LIMITE_GRATUITE} analyses restantes ce mois")
    if restantes == 0:
        st.warning("Limite atteinte. Passe au plan premium pour continuer.")
        st.markdown("💳 **Contact pour passer premium :** +226 57 63 85 14 (Orange Money / Moov Money)")

st.markdown("---")

niches_toutes = ["humour", "lifestyle", "education", "gaming", "business"]
niches_gratuites = ["humour"]

onglet1, onglet2 = st.tabs(["📈 Hashtags", "🕐 Horaires de publication"])

with onglet1:
    st.write("Découvrez les meilleurs hashtags pour votre niche.")
    options_niches = niches_toutes if (est_premium or restantes > 0) else niches_gratuites
    niche = st.selectbox("Choisissez votre niche :", options_niches)

    if st.button("Obtenir les hashtags", key="hashtags"):
        if not est_premium and restantes == 0:
            st.error("Limite gratuite atteinte pour ce mois.")
        else:
            resultats = suggerer_hashtags(niche)
            st.success(f"Hashtags suggérés pour **{niche}** :")
            for tag in resultats:
                st.write(f"- {tag}")

            if not est_premium:
                incrementer_utilisation(profil["id"], utilisees)
                st.session_state.profil["analyses_utilisees_ce_mois"] = utilisees + 1
                st.rerun()

with onglet2:
    st.write("Trouvez les meilleurs créneaux pour publier.")
    jour = st.selectbox(
        "Choisissez le jour :",
        ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"],
    )
    if st.button("Obtenir les créneaux", key="scheduler"):
        creneaux = obtenir_creneaux(jour)
        st.success(f"Meilleurs créneaux pour **{jour}** :")
        for c in creneaux:
            st.write(f"- {c}")

st.markdown("---")
st.caption("Cet outil ne génère aucune vue, like ou interaction artificielle. Il aide uniquement à optimiser votre stratégie de publication, de façon 100% organique.")

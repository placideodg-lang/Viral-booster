import streamlit as st
from hashtags import suggerer_hashtags
from scheduler import obtenir_creneaux
from supabase import create_client
from datetime import datetime, timezone
import re

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

supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_ANON_KEY"])

LIMITE_GRATUITE = 3


def parser_date_supabase(valeur_date):
    if not valeur_date:
        return datetime.now(timezone.utc)
    try:
        nettoye = re.sub(r"\.\d+", "", valeur_date)
        nettoye = nettoye.replace("Z", "+00:00")
        if "+" not in nettoye:
            nettoye += "+00:00"
        return datetime.fromisoformat(nettoye)
    except Exception:
        return datetime.now(timezone.utc)

def obtenir_profil(user_id):
    try:
        reponse = supabase.table("profiles").select("*").eq("id", user_id).execute()
        st.write("DEBUG - reponse brute:", reponse.data)
        if reponse.data and len(reponse.data) > 0:
            return reponse.data[0]
        else:
            st.error("DEBUG: aucune ligne retournee pour cet id")
            return None
    except Exception as e:
        st.error(f"DEBUG erreur profil : {e}")
        return None


def verifier_et_reinitialiser_compteur(profil):
    dernier_reset = parser_date_supabase(profil.get("date_dernier_reset"))
    maintenant = datetime.now(timezone.utc)

    if maintenant.month != dernier_reset.month or maintenant.year != dernier_reset.year:
        try:
            supabase.table("profiles").update({
                "analyses_utilisees_ce_mois": 0,
                "date_dernier_reset": maintenant.isoformat(),
            }).eq("id", profil["id"]).execute()
        except Exception:
            pass
        profil["analyses_utilisees_ce_mois"] = 0

    return profil


def incrementer_utilisation(user_id, valeur_actuelle):
    try:
        supabase.table("profiles").update({
            "analyses_utilisees_ce_mois": valeur_actuelle + 1
        }).eq("id", user_id).execute()
    except Exception:
        pass


if "utilisateur" not in st.session_state:
    st.session_state.utilisateur = None
if "profil" not in st.session_state:
    st.session_state.profil = None

st.title("🚀 Amplificateur Viral")
st.subheader("Outil d'aide à la croissance TikTok")

if st.session_state.utilisateur is None:
    st.markdown("---")
    onglet_connexion, onglet_inscription = st.tabs(["Se connecter", "Créer un compte"])

    with onglet_connexion:
        email = st.text_input("Email", key="email_connexion").strip()
        mot_de_passe = st.text_input("Mot de passe", type="password", key="mdp_connexion")
        if st.button("Se connecter"):
            if not email or not mot_de_passe:
                st.error("Merci de remplir l'email et le mot de passe.")
            else:
                try:
                    resultat = supabase.auth.sign_in_with_password({"email": email, "password": mot_de_passe})
                    profil = obtenir_profil(resultat.user.id)
                    if profil is None:
                        st.error("Compte trouvé mais profil introuvable. Contacte le support.")
                    else:
                        st.session_state.utilisateur = resultat.user
                        st.session_state.profil = profil
                        st.rerun()
                except Exception as e:
                    st.error(f"Connexion impossible : email ou mot de passe incorrect.")
                    with st.expander("Détails techniques (pour le support)"):
                        st.code(str(e))

    with onglet_inscription:
        nom = st.text_input("Nom complet", key="nom_inscription").strip()
        email_i = st.text_input("Email", key="email_inscription").strip()
        mdp_i = st.text_input("Mot de passe", type="password", key="mdp_inscription")
        if st.button("Créer mon compte"):
            if not email_i or not mdp_i:
                st.error("Merci de remplir tous les champs.")
            elif len(mdp_i) < 6:
                st.error("Le mot de passe doit contenir au moins 6 caractères.")
            else:
                try:
                    supabase.auth.sign_up({
                        "email": email_i,
                        "password": mdp_i,
                        "options": {"data": {"nom_complet": nom}}
                    })
                    st.success("✅ Compte créé ! Tu peux maintenant te connecter dans l'onglet 'Se connecter'.")
                except Exception as e:
                    st.error(f"Erreur lors de la création du compte : {e}")

    st.stop()

profil = verifier_et_reinitialiser_compteur(st.session_state.profil)
est_premium = profil.get("statut_abonnement") == "premium"
utilisees = profil.get("analyses_utilisees_ce_mois", 0) or 0
restantes = max(0, LIMITE_GRATUITE - utilisees)

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"Connecté en tant que **{profil.get('nom_complet') or profil.get('email')}**")
with col2:
    if st.button("Déconnexion"):
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
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

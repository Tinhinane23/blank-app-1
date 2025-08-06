import streamlit as st
import pandas as pd
import json

# Configuration de la page
st.set_page_config(page_title="Macro Process – Simulateur", layout="wide")

# Titre
st.title("🪩 Macro Process – Simulateur de briques")
st.caption("Sélectionnez, organisez et exportez vos briques d'activité et de production")

# Liste des briques extraites du fichier HTML
briques = [
    "Discours Facteur", "Questions du facteur et saisie des réponses", "Saisie d'une information",
    "Prise de photos", "Vérification d'identité", "Réalisation d'un contrôle sans manipulation",
    "Réalisation d'un contrôle avec manipulation", "Prise de mesures et saisie du résultat",
    "Retrait des produits alimentaires non conformes", "Remontée d'alerte",
    "Collecte alimentaire (température froid positif)", "Collecte alimentaire (température ambiante)",
    "Collecte d'objets et matériels", "Collecte d'UM et de contenants", "Collecte commentée",
    "Livraison alimentaire (température froid positif)", "Livraison alimentaire (température ambiante)",
    "Livraison d'objets et matériels", "Livraison d'UM et contenants", "Remise commentée",
    "Dépôt alimentaire (froid positif)", "Dépôt de matériel par le client",
    "Dépôt en PIC par le client et acheminement", "Retrait alimentaire (froid positif)",
    "Retrait alimentaire (température ambiante)", "Retrait de matériel par le client",
    "Installation de matériel", "Désinstallation de matériel", "Échange (objets, plis…)",
    "Mise sous plis", "Préparation de commande", "Préparation de commande (fresh)",
    "Prise de rdv par l'établissement postal", "Prise de rdv par le facteur en tournée",
    "Entrée en stock", "Stockage (flux standards et sécurisés)", "Entreposage et transit (fresh)",
    "Inventaire", "Flashage", "Recueil d'une signature", "Etiquetage",
    "Réception flux postal", "Réception flux client", "Ventilation des flux", "Expédition",
    "Traitement de la prestation par la PIC Arrivée et acheminement", "Consultation de la prestation",
    "Affectation de la prestation", "Préparation de la prestation en Production",
    "Préparation de la prestation Fresh en Production", "Préparation de la prestation en cabine",
    "Réalisation du départ en tournée", "Ouverture de la mission", "Pilotage de la prestation",
    "Appel facteur en mission", "Clôture de la mission",
    "Traitement de la prestation en Production au retour de tournée",
    "Traitement de la prestation FRESH en Production au retour de tournée",
    "Traitement de la prestation en cabine en retour de tournée", "Nettoyage",
    "Tri pour distribution", "Tri pour dispersion", "Préparation du chantier", "Dégroupage",
    "Cas d'échec", "Cas d'échec alimentaire"
]

df_briques = pd.DataFrame(briques, columns=["Nom"])
df_briques["Catégorie"] = "Activité"

# Initialisation de la session
if "briques_selectionnees" not in st.session_state:
    st.session_state.briques_selectionnees = pd.DataFrame(columns=["Nom", "Catégorie"])

# Interface principale
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📋 Briques disponibles")
    selected = st.selectbox("Choisir une brique à ajouter", df_briques["Nom"])
    if st.button("➕ Ajouter la brique"):
        if selected not in st.session_state.briques_selectionnees["Nom"].values:
            brique = df_briques[df_briques["Nom"] == selected].iloc[0]
            st.session_state.briques_selectionnees = pd.concat(
                [st.session_state.briques_selectionnees, pd.DataFrame([brique])], ignore_index=True
            )
            st.success(f"Brique ajoutée : {selected}")
        else:
            st.warning("Cette brique est déjà ajoutée.")

    st.subheader("🧱 Briques sélectionnées")
    if st.session_state.briques_selectionnees.empty:
        st.info("Aucune brique sélectionnée.")
    else:
        for i, row in st.session_state.briques_selectionnees.iterrows():
            with st.expander(f"{row['Nom']}", expanded=True):
                if st.button("❌ Supprimer", key=f"suppr_{i}"):
                    st.session_state.briques_selectionnees.drop(i, inplace=True)
                    st.session_state.briques_selectionnees.reset_index(drop=True, inplace=True)
                    st.rerun()

with col2:
    st.subheader("📊 Résumé de la mission")
    if st.session_state.briques_selectionnees.empty:
        st.info("Ajoutez des briques pour afficher le résumé.")
    else:
        st.dataframe(st.session_state.briques_selectionnees)

        # Export CSV
        csv = st.session_state.briques_selectionnees.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Télécharger CSV", csv, file_name="macro_process.csv", mime="text/csv")

        # Export JSON
        json_data = st.session_state.briques_selectionnees.to_dict(orient="records")
        json_str = json.dumps(json_data, indent=2)
        st.download_button("⬇️ Télécharger JSON", json_str, file_name="macro_process.json", mime="application/json")

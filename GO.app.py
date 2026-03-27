import streamlit as st
import pandas as pd
import re

# 1. Configuration de la page
st.set_page_config(page_title="Coach Grand Oral", page_icon="🎓", layout="wide")

# 2. Fonction pour les images Google Drive
def get_drive_direct_link(url):
    if pd.isna(url) or "drive.google.com" not in str(url):
        return url
    file_id = re.search(r'/d/([a-zA-Z0-9-_]+)', str(url))
    if file_id:
        return f"https://drive.google.com/uc?export=view&id={file_id.group(1)}"
    return url

# 3. Identifiant de ton Google Sheet
SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet="

st.title("🎓 Coach Grand Oral")

# 4. Navigation (Menu latéral)
menu = st.sidebar.radio("Navigation", 
    ["Home", "Compétences fondamentales", "ZEN", "Exercices ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

# 5. Chargement et Affichage
try:
    # On prépare l'URL de l'onglet sélectionné
    onglet_nom = menu.replace(" ", "%20")
    df = pd.read_csv(BASE_URL + onglet_nom)
    df = df.fillna("") # Remplace les cases vides pour éviter les bugs

    if menu == "Home":
        for _, row in df.iterrows():
            if row.get('Nom'): st.header(row['Nom'])
            if 'Image' in df.columns and row['Image'] != "":
                st.image(get_drive_direct_link(row['Image']), use_container_width=True)
            for t in ['texte', 'texte 1', 'texte 2', 'texte 3', 'texte 4']:
                if t in df.columns and row[t] != "": st.write(row[t])

    elif menu == "Compétences fondamentales":
        st.header("Les Fondamentaux")
        for _, row in df.iterrows():
            with st.container(border=True):
                if 'Image' in df.columns and row['Image'] != "": 
                    st.image(get_drive_direct_link(row['Image']), width=400)
                if 'texte' in df.columns: st.info(row['texte'])

    elif menu == "ZEN":
        st.header("Plan ZEN")
        for _, row in df.iterrows():
            with st.expander(f"🧘 {row.get('nom', 'Exercice')}", expanded=True):
                c1, c2 = st.columns([1, 2])
                with c1:
                    if 'logo' in df.columns and row['logo'] != "":
                        st.image(get_drive_direct_link(row['logo']), width=150)
                with c2:
                    if 'texte' in df.columns: st.write(row['texte'])
                if 'image' in df.columns and row['image'] != "":
                    st.image(get_drive_direct_link(row['image']), use_container_width=True)

    elif "Exercices" in menu:
        st.header(menu)
        for _, row in df.iterrows():
            with st.expander(f"🎯 {row.get('nom', 'Détails')}"):
                if 'descriptif' in df.columns: st.write(f"**Objectif :** {row['descriptif']}")
                st.divider()
                if 'Exercice' in df.columns: st.write(row['Exercice'])
                if 'video' in df.columns and row['video'] != "":
                    st.video(row['video'])
                if 'image' in df.columns and row['image'] != "":
                    st.image(get_drive_direct_link(row['image']))

    elif menu == "Countdown":
        st.header("⏳ Dernières étapes")
        for _, row in df.iterrows():
            st.subheader(f"🗓️ {row.get('nom', '')}")
            cols = st.columns(2)
            with cols[0]:
                for t in ['texte', 'texte 1', 'texte 2', 'texte 3', 'texte 4', 'texte 5']:
                    if t in df.columns and row[t] != "": st.write(f"✅ {row[t]}")
            with cols[1]:
                if 'Conseil' in df.columns and row['Conseil'] != "":
                    st.success(f"💡 Conseil : {row['Conseil']}")
                if 'Détente' in df.columns and row['Détente'] != "":
                    st.info(f"🧘 Détente : {row['Détente']}")
                if 'affaires' in df.columns and row['affaires'] != "":
                    st.warning(f"🎒 Affaires : {row['affaires']}")
            st.divider()

except Exception as e:
    st.error(f"Erreur d'accès aux données : {e}")
    st.info("Vérifie que ton Google Sheet est bien PARTAGÉ en mode 'Tous les utilisateurs avec le lien'.")

st.sidebar.markdown("---")
st.sidebar.caption("Coach Grand Oral v1.0")

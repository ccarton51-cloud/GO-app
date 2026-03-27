import streamlit as st
import pandas as pd
import re

# Configuration de la page
st.set_page_config(page_title="Coach Grand Oral", page_icon="🎓", layout="wide")

# --- FONCTIONS UTILES ---
def get_drive_direct_link(url):
    """Transforme un lien Google Drive standard en lien image direct"""
    if pd.isna(url) or "drive.google.com" not in str(url):
        return url
    file_id = re.search(r'/d/([a-zA-Z0-9-_]+)', str(url))
    if file_id:
        return f"https://drive.google.com/uc?export=view&id={file_id.group(1)}"
    return url

# Identifiant de ton Google Sheet
SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet="

st.title("🎓 Coach Grand Oral")

# --- NAVIGATION ---
menu = st.sidebar.radio("Navigation", 
    ["Home", "Compétences fondamentales", "ZEN", "Exercices ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

# --- CHARGEMENT ET AFFICHAGE ---
try:
    # Encodage du nom de l'onglet pour l'URL
    onglet_url = menu.replace(" ", "%20")
    df = pd.read_csv(BASE_URL + onglet_url)

    if menu == "Home":
        for _, row in df.iterrows():
            st.header(row.get('Nom', ''))
            if 'Image' in df.columns and pd.notna(row['Image']):
                st.image(get_drive_direct_link(row['Image']), use_container_width=True)
            for t in ['texte', 'texte 1', 'texte 2', 'texte 3', 'texte 4']:
                if t in df.columns and pd.notna(row[t]): st.write(row[t])

    elif menu == "Compétences fondamentales":
        for _, row in df.iterrows():
            with st.container(border=True):
                if 'Image' in df.columns and pd.notna(row['Image']): 
                    st.image(get_drive_direct_link(row['Image']), width=400)
                st.info(row.get('texte', ''))

    elif menu == "ZEN":
        for _, row in df.iterrows():
            with st.expander(f"🧘 {row.get('nom', 'Exercice')}", expanded=True):
                c1, c2 = st.columns([1, 2])
                with c1:
                    if 'logo' in df.columns and pd.notna(row['logo']):
                        st.image(get_drive_direct_link(row['logo']), width=150)
                with c2:
                    st.write(row.get('texte', ''))
                if 'image' in df.columns and pd.notna(row['image']):
                    st.image(get_drive_direct_link(row['image']), use_container_width=True)

    elif "Exercices" in menu:
        for _, row in df.iterrows():
            with st.expander(f"🎯 {row.get('nom', 'Détails')}"):
                if 'descriptif' in df.columns: st.write(f"**Objectif :** {row['descriptif']}")
                st.divider()
                if 'Exercice' in df.columns: st.write(row['Exercice'])
                if 'video' in df.columns and pd.notna(row['video']):
                    st.video(row['video'])
                if 'image' in df.columns and pd.notna(row['image']):
                    st.image(get_drive_direct_link(row['image']))

    elif menu == "Countdown":
        for _, row in df.iterrows():
            st.subheader(f"🗓️ {row.get('nom', '')}")
            cols = st.columns(2)
            with cols[0]:
                st.write("**Préparation :**")
                for t in ['texte', 'texte 1', 'texte 2', 'texte 3']:
                    if t in df.columns and pd.notna(row[t]): st.write(f"- {row[t]}")
            with cols[1]:
                if 'Conseil' in df.columns and pd.notna(row['Conseil']):
                    st.success(f"💡 {row['Conseil']}")
                if 'Détente' in df.columns and pd.notna(row['Détente']):
                    st.info(f"🧘 {row['Détente']}")
            st.divider()

except Exception as e:
    st.error(f"Erreur de chargement : {e}")
    st.info("Vérifie que l'onglet existe bien dans ton Google Sheet.")

st.sidebar.markdown("---")
st.sidebar.caption("Application créée pour accompagner tes élèves.")

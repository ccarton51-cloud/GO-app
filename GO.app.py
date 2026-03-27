import streamlit as st
import pandas as pd
import re

# Configuration
st.set_page_config(page_title="Coach Grand Oral", page_icon="🎓", layout="wide")

# --- FONCTIONS UTILES ---
def get_drive_direct_link(url):
    if pd.isna(url) or "drive.google.com" not in str(url): return url
    file_id = re.search(r'/d/([a-zA-Z0-9-_]+)', str(url))
    return f"https://drive.google.com/uc?export=view&id={file_id.group(1)}" if file_id else url

# URL de ton Sheet (format export multi-onglets)
SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet="

# --- INTERFACE ---
st.title("🎓 Coach Grand Oral")

# Navigation calquée sur tes onglets
menu = st.sidebar.radio("Navigation", 
    ["Accueil", "Compétences fondamentales", "Plan ZEN", "Exercices (Ethos/Logos/Pathos)", "Compte à rebours"])

try:
    if menu == "Accueil":
        df = pd.read_csv(BASE_URL + "Home")
        for _, row in df.iterrows():
            st.header(row['Nom'])
            if 'Image' in df.columns: st.image(get_drive_direct_link(row['Image']))
            st.write(row.get('texte', ''))
            st.write(row.get('texte 1', ''))

    elif menu == "Compétences fondamentales":
        df = pd.read_csv(BASE_URL + "Compétences%20fondamentales")
        col1, col2 = st.columns(2)
        for i, row in df.iterrows():
            with st.expander(f"💡 Conseil {i+1}"):
                if 'Image' in df.columns: st.image(get_drive_direct_link(row['Image']))
                st.write(row.get('texte', ''))

    elif menu == "Plan ZEN":
        df = pd.read_csv(BASE_URL + "ZEN")
        for _, row in df.iterrows():
            with st.container(border=True):
                st.subheader(row['nom'])
                cols = st.columns([1, 2])
                with cols[0]:
                    if 'logo' in df.columns: st.image(get_drive_direct_link(row['logo']), width=100)
                with cols[1]:
                    st.write(row.get('texte', ''))
                if 'image' in df.columns: st.image(get_drive_direct_link(row['image']))

    elif menu == "Exercices (Ethos/Logos/Pathos)":
        onglet = st.selectbox("Choisir la catégorie", ["Exercices ETHOS", "Exercices LOGOS", "Exercices PATHOS"])
        df = pd.read_csv(BASE_URL + onglet.replace(" ", "%20"))
        for _, row in df.iterrows():
            with st.expander(f"🎯 {row['nom']}"):
                st.write(f"**Description :** {row['descriptif']}")
                st.info(f"**L'exercice :** \n\n {row['Exercice']}")

    elif menu == "Compte à rebours":
        df = pd.read_csv(BASE_URL + "Countdown")
        for _, row in df.iterrows():
            st.warning(f"🗓️ {row['nom']}")
            st.write(row.get('texte 1', ''))
            st.write(row.get('texte 2', ''))

except Exception as e:
    st.error(f"Note : L'onglet '{menu}' demande un ajustement ou est en cours de mise à jour.")
    st.info("Vérifie que le nom de l'onglet dans ton Google Sheet est exactement le même que dans le code.")

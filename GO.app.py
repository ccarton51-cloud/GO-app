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

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 5px; padding: 10px; }
    .exercice-box { border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin-bottom: 10px; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Coach Grand Oral")

# --- NAVIGATION ---
# J'ai repris exactement l'ordre de tes onglets
menu = st.sidebar.radio("Navigation", 
    ["Home", "Compétences fondamentales", "ZEN", "Exercices ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

try:
    if menu == "Home":
        df = pd.read_csv(BASE_URL + "Home")
        for _, row in df.iterrows():
            st.header(row.get('Nom', 'Accueil'))
            if 'Image' in df.columns: st.image(get_drive_direct_link(row['Image']), use_container_width=True)
            for t in ['texte', 'texte 1', 'texte 2', 'texte 3', 'texte 4']:
                if t in df.columns and pd.notna(row[t]): st.write(row[t])

    elif menu == "Compétences fondamentales":
        df = pd.read_csv(BASE_URL + "Compétences%20fondamentales")
        st.header("Les Fondamentaux")
        for _, row in df.iterrows():
            if 'Image' in df.columns and pd.notna(row['Image']): 
                st.image(get_drive_direct_link(row['Image']), width=300)
            st.info(row.get('texte', ''))

    elif menu == "ZEN":
        df = pd.read_csv(BASE_URL + "ZEN")
        st.header("Plan ZEN")
        for _, row in df.iterrows():
            with st.container():
                st.subheader

import streamlit as st
import pandas as pd
import re

# 1. Configuration de la page
st.set_page_config(page_title="Coach Grand Oral", page_icon="🎓", layout="wide")

# 2. Fonction magique pour nettoyer les liens (GitHub et Drive)
def get_link(url):
    if pd.isna(url) or str(url).strip() == "": 
        return None
    
    url = str(url).strip()
    
    # Transformation pour GitHub (on veut le contenu brut/raw)
    if "github.com" in url and "raw" not in url:
        url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    
    # Transformation pour Google Drive (au cas où il en reste)
    if "drive.google.com" in url:
        file_id = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
        if file_id: 
            return f"https://drive.google.com/uc?export=view&id={file_id.group(1)}"
    
    return url

# 3. Paramètres de ton Google Sheet
SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet="

st.title("🎓 Coach Grand Oral")

# 4. Navigation latérale
menu = st.sidebar.radio("Navigation", 
    ["Home", "Compétences fondamentales", "ZEN", "Exercices ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

try:
    # Chargement de l'onglet correspondant
    onglet_nom = menu.replace(" ", "%20")
    df = pd.read_csv(BASE_URL + onglet_nom).fillna("")
    
    # On force les noms de colonnes en minuscules pour éviter les erreurs de frappe
    df.columns = [c.strip().lower() for c in df.columns]

    # --- BOUCLE D'AFFICHAGE DES LIGNES ---
    for i, row in df.iterrows():
        # Titre de la section
        if 'nom' in df.columns and row['nom']:
            st.header(row['nom'])
        
        # Affichage du texte principal (colonne 'texte')
        if 'texte' in df.columns and row['texte']:
            st.write(row['texte'])

        # --- GESTION DES IMAGES ---
        if 'image' in df.columns and row['image']:
            img_url = get_link(row['image'])
            if img_url:
                # Affiche l'image. Si le lien GitHub est bon, ça marche direct.
                st.image(img_url, use

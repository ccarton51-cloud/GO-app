import streamlit as st
import pandas as pd
import re

# 1. Configuration de la page
st.set_page_config(page_title="Coach Grand Oral", page_icon="🎓", layout="wide")

# 2. Fonction pour nettoyer les liens
def get_link(url):
    if pd.isna(url) or str(url).strip() == "": 
        return None
    
    url = str(url).strip()
    
    # Transformation GitHub (Lien Direct)
    if "github.com" in url and "raw" not in url:
        url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    
    # Transformation Google Drive
    if "drive.google.com" in url:
        file_id = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
        if file_id: 
            return f"https://drive.google.com/uc?export=view&id={file_id.group(1)}"
    
    return url

# 3. Paramètres Google Sheet
SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet="

st.title("🎓 Coach Grand Oral")

# 4. Navigation
menu = st.sidebar.radio("Navigation", 
    ["Home", "Compétences fondamentales", "ZEN", "Exercices ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

try:
    # Chargement des données
    onglet_nom = menu.replace(" ", "%20")
    df = pd.read_csv(BASE_URL + onglet_nom).fillna("")
    df.columns = [c.strip().lower() for c in df.columns]

    for i, row in df.iterrows():
        # Titre
        if 'nom' in df.columns and row['nom']:
            st.header(row['nom'])
        
        # Texte principal
        if 'texte' in df.columns and row['texte']:
            st.write(row['texte'])

        # --- GESTION DES IMAGES (Ligne corrigée ici) ---
        if 'image' in df.columns and row['image']:
            img_url = get_link(row['image'])
            if img_url:
                st.image(img_url, use_container_width=True)
        
        # Vidéos
        if 'video' in df.columns and row['video']:
            st.video(row['video'])
            
        # Conseils
        if 'conseil' in df.columns and row['conseil']:
            st.success(row['conseil'])

        # Textes additionnels
        for c in df.columns:
            if any(x in c for x in ['1','2','3']) and row[c] != "":
                st.write(row[c])
        
        st.divider()

except Exception as e:
    st.error(f"Erreur de chargement : {e}")

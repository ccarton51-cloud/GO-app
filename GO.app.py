import streamlit as st
import pandas as pd
import re

# 1. Configuration
st.set_page_config(page_title="Coach Grand Oral", page_icon="🎓", layout="wide")

def get_link(url):
    if pd.isna(url) or str(url).strip() == "" or str(url).strip() == "0": 
        return None
    url = str(url).strip()
    # Conversion automatique GitHub vers lien direct (Raw)
    if "github.com" in url and "raw" not in url:
        url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    # Conversion Drive
    if "drive.google.com" in url:
        file_id = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
        if file_id: return f"https://drive.google.com/uc?export=view&id={file_id.group(1)}"
    return url

# 2. Connexion Sheet
SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet="

st.title("🎓 Coach Grand Oral")

# 3. Menu
menu = st.sidebar.radio("Navigation", 
    ["Home", "Compétences fondamentales", "ZEN", "Exercices ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

try:
    onglet_nom = menu.replace(" ", "%20")
    # On force pandas à ne pas interpréter les colonnes vides comme des 0
    df = pd.read_csv(BASE_URL + onglet_nom).fillna("")
    df.columns = [c.strip().lower() for c in df.columns]

    for i, row in df.iterrows():
        # Affichage du nom/titre
        nom_section = str(row.get('nom', '')).strip()
        if nom_section and nom_section != "0":
            st.header(nom_section)
        
        # Affichage du texte
        texte_principal = str(row.get('texte', '')).strip()
        if texte_principal and texte_principal != "0":
            st.write(texte_principal)

        # --- AFFICHAGE DE L'IMAGE ---
        # On vérifie si la colonne 'image' existe et contient quelque chose
        if 'image' in df.columns:
            valeur_image = str(row['image']).strip()
            if valeur_image and valeur_image != "0":
                img_url = get_link(valeur_image)
                if img_url:
                    # Ici, st.image affiche l'image, pas le lien !
                    st.image(img_url, use_container_width=True)

        # Vidéo
        if 'video' in df.columns and str(row['video']).strip() not in ["", "0"]:
            st.video(row['video'])
            
        # Textes secondaires (1, 2, 3)
        for c in ['texte1', 'texte2', 'texte3']:
            if c in df.columns:
                val = str(row[c]).strip()
                if val and val != "0":
                    st.write(val)
        
        st.divider()

except Exception as e:
    st.error(f"Erreur : {e}")

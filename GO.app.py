import streamlit as st
import pandas as pd
import re

# 1. Configuration
st.set_page_config(page_title="Coach Grand Oral", page_icon="🎓", layout="wide")

def get_link(url):
    if pd.isna(url) or str(url).strip() in ["", "0", "nan"]: 
        return None
    url = str(url).strip()
    # Conversion automatique GitHub vers Raw
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
    df = pd.read_csv(BASE_URL + onglet_nom).fillna("")
    # Nettoyage des noms de colonnes
    df.columns = [c.strip().lower() for c in df.columns]

    for i, row in df.iterrows():
        # --- TITRE ---
        nom_section = str(row.get('nom', '')).strip()
        if nom_section and nom_section != "0":
            st.header(nom_section)
        
        # --- TEXTE PRINCIPAL ---
        texte_p = str(row.get('texte', '')).strip()
        if texte_p and texte_p != "0":
            st.write(texte_p)

        # --- GESTION DES IMAGES (Toutes les colonnes contenant "image") ---
        # On crée des colonnes Streamlit si on a plusieurs images (image 1, image 2)
        cols_img = [c for c in df.columns if 'image' in c]
        
        if cols_img:
            # On filtre les liens valides pour ne pas créer de colonnes vides
            liens_valides = []
            for c in cols_img:
                link = get_link(row[c])
                if link: liens_valides.append(link)
            
            if liens_valides:
                # Si on a plusieurs images, on les affiche côte à côte
                if len(liens_valides) > 1:
                    st_cols = st.columns(len(liens_valides))
                    for idx, link in enumerate(liens_valides):
                        st_cols[idx].image(link, use_container_width=True)
                else:
                    st.image(liens_valides[0], use_container_width=True)

        # --- VIDÉO ---
        if 'video' in df.columns and str(row['video']).strip() not in ["", "0"]:
            st.video(row['video'])
            
        # --- TEXTES SECONDAIRES ---
        for c in df.columns:
            if ('texte' in c and c != 'texte') and str(row[c]).strip() not in ["", "0"]:
                st.write(str(row[c]).strip())
        
        st.divider()

except Exception as e:
    st.error(f"Erreur : {e}")

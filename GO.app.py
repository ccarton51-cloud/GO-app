import streamlit as st
import pandas as pd
import re
import urllib.parse

# 1. Configuration de la page (Favicon Chrome)
LOGO_PAR_DEFAUT = "https://raw.githubusercontent.com/ccarton51-cloud/GO-app/main/images/logo.png"
st.set_page_config(page_title="Coach Grand Oral", page_icon=LOGO_PAR_DEFAUT, layout="wide")

def get_link(url):
    if pd.isna(url) or len(str(url)) < 10 or not str(url).strip().lower().startswith('http'): 
        return None
    url = str(url).strip()
    # Nettoyage automatique des liens GitHub
    if "github.com" in url and "raw" not in url:
        url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    return url

# 2. Paramètres Google Sheet
SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet="

# Titre de l'application
st.title("Coach Grand Oral")

# 3. Navigation
menu = st.sidebar.radio("Navigation", 
    ["Home", "L'épreuve", "Compétences fondamentales", "ZEN", "Exercices ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

# --- CHARGEMENT DES DONNÉES ---
try:
    onglet_encode = urllib.parse.quote(menu)
    df = pd.read_csv(BASE_URL + onglet_encode).fillna("")
    df.columns = [c.strip().lower() for c in df.columns]

    # --- CAS PARTICULIER : PAGE HOME ---
    if menu == "Home":
        # On cherche l'image dans 'image 1' pour le logo de bienvenue
        img_home = LOGO_PAR_DEFAUT
        if 'image 1' in df.columns:
            link = get_link(df['image 1'].iloc[0])
            if link: img_home = link
        
        st.image(img_home, width=200)
        
        # Affichage du texte de bienvenue (colonne 'texte')
        if 'texte' in df.columns:
            st.markdown(df['texte'].iloc[0])

    # --- CAS GÉNÉRAL : AUTRES PAGES ---
    else:
        for i, row in df.iterrows():
            # 1. Titre de section (colonne 'nom')
            if 'nom' in df.columns and str(row['nom']).strip() not in ["", "0", "nan"]:
                st.header(row['nom'])
            
            # 2. Texte de section (colonne 'texte')
            if 'texte' in df.columns and str(row['texte']).strip() not in ["", "0", "nan"]:
                st.write(row['texte'])

            # 3. Images (côte à côte si image 1 et image 2 sont remplies)
            liens_valides = []
            for col_name in ['image 1', 'image 2', 'image 3']:
                if col_name in df.columns:
                    l = get_link(row[col_name])
                    if l: liens_valides.append(l)
            
            if liens_valides:
                if len(liens_valides) > 1:
                    cols = st.columns(len(liens_valides))
                    for idx, link in enumerate(liens_valides):
                        cols[idx].image(link, use_container_width=True)
                else:
                    st.image(liens_valides[0], use_container_width=True)

            # 4. Vidéo
            if 'video' in df.columns and str(row['video']).startswith('http'):
                st.video(row['video'])
            
            st.divider()

except Exception as e:
    st.info("Sélectionnez une section ou vérifiez que l'onglet existe dans votre Google Sheet.")

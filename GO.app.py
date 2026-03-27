import streamlit as st
import pandas as pd
import re
import urllib.parse

# 1. Configuration de la page
LOGO_URL = "https://raw.githubusercontent.com/ccarton51-cloud/GO-app/main/images/logo.png"
st.set_page_config(page_title="Coach Grand Oral", page_icon=LOGO_URL, layout="wide")

def get_link(url):
    if pd.isna(url) or len(str(url)) < 10 or not str(url).strip().lower().startswith('http'): 
        return None
    url = str(url).strip()
    if "github.com" in url and "raw" not in url:
        url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    return url

# 2. Paramètres Google Sheet
SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet="

st.title("Coach Grand Oral")

# 3. Menu
menu = st.sidebar.radio("Navigation", 
    ["Home", "L'épreuve", "Compétences fondamentales", "ZEN", "Exercices ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

# --- PAGE ACCUEIL (HOME) ---
if menu == "Home":
    try:
        # On va quand même chercher l'image dans le Sheet pour l'onglet Home
        df_home = pd.read_csv(BASE_URL + "Home").fillna("")
        df_home.columns = [c.strip().lower() for c in df_home.columns]
        
        # On affiche l'image de la colonne 'image' si elle existe
        if 'image' in df_home.columns:
            img_home = get_link(df_home['image'].iloc[0])
            if img_home:
                st.image(img_home, width=200)
            else:
                st.image(LOGO_URL, width=200) # Backup si lien mort
    except:
        st.image(LOGO_URL, width=200) # Backup si onglet Home introuvable

    st.markdown("""
    Bienvenue dans ton allié ultime pour réussir le Grand Oral.  
    Cette application a été conçue comme un véritable aide-mémoire, simple et efficace... [Ton texte]
    """)

# --- AUTRES PAGES (L'épreuve, etc.) ---
else:
    try:
        onglet_encode = urllib.parse.quote(menu)
        df = pd.read_csv(BASE_URL + onglet_encode).fillna("")
        df.columns = [c.strip().lower() for c in df.columns]

        for i, row in df.iterrows():
            # Titre
            nom = str(row.get('nom', '')).strip()
            if nom and nom not in ["0", "nan"]:
                st.header(nom)
            
            # Texte
            txt = str(row.get('texte', '')).strip()
            if txt and txt not in ["0", "nan"]:
                st.write(txt)

            # --- LOGIQUE D'IMAGE SÉLECTIVE ---
            # Sur ces pages, on ignore la colonne 'image' et on ne prend que 'image 1' et 'image 2'
            liens_valides = []
            for col_name in ['image 1', 'image 2']:
                if col_name in df.columns:
                    link = get_link(row[col_name])
                    if link:
                        liens_valides.append(link)
            
            if liens_valides:
                if len(liens_valides) > 1:
                    cols = st.columns(len(liens_valides))
                    for idx, l in enumerate(liens_valides):
                        cols[idx].image(l, use_container_width=True)
                else:
                    st.image(liens_valides[0], use_container_width=True)

            # Vidéo
            if 'video' in df.columns and str(row['video']).startswith('http'):
                st.video(row['video'])

            st.divider()

    except Exception as e:
        st.error("Erreur de chargement de l'onglet.")

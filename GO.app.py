import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuration
st.set_page_config(page_title="Coach Grand Oral", layout="wide")

def get_link(url):
    if pd.isna(url) or len(str(url)) < 10: return None
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
    ["Home", "L'épreuve", "Compétences fondamentales", "ZEN", "L'ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

# --- CHARGEMENT SANS CACHE POUR FORCER LA MISE À JOUR ---
try:
    url = BASE_URL + urllib.parse.quote(menu)
    df = pd.read_csv(url).fillna("")
    df.columns = [c.strip().lower() for c in df.columns]

    # --- LOGIQUE POUR L'ETHOS ---
    if menu == "L'ETHOS":
        for i, row in df.iterrows():
            # On ne traite que les lignes qui ont un NOM (pour éviter les lignes vides du Sheet)
            nom_val = str(row.get('nom', '')).strip()
            if nom_val and nom_val.lower() not in ["0", "nan", ""]:
                # 1. NOM
                st.header(nom_val)
                
                # 2. IMAGE (colonne logo)
                if 'logo' in df.columns:
                    img = get_link(row['logo'])
                    if img:
                        st.image(img, width=600)
                
                # 3. DESCRIPTIF
                if 'descriptif' in df.columns:
                    desc = str(row['descriptif']).strip()
                    if desc and desc.lower() not in ["0", "nan", ""]:
                        st.markdown(f"**Note :** {desc}")
                
                # 4. EXERCICE
                if 'exercice' in df.columns:
                    exo = str(row['exercice']).strip()
                    if exo and exo.lower() not in ["0", "nan", ""]:
                        st.info(f"**L'exercice :**\n\n{exo}")
                
                st.divider()

    # --- LOGIQUE POUR LA HOME ---
    elif menu == "Home":
        st.image("https://raw.githubusercontent.com/ccarton51-cloud/GO-app/main/images/logo.png", width=200)
        st.write("Bienvenue dans ton allié ultime pour réussir le Grand Oral...")

    # --- LOGIQUE POUR LES AUTRES PAGES ---
    else:
        for i, row in df.iterrows():
            nom_val = str(row.get('nom', '')).strip()
            if nom_val and nom_val.lower() not in ["0", "nan", ""]:
                st.header(nom_val)
                
                if 'texte' in df.columns:
                    st.write(row['texte'])

                for col in ['image 1', 'image 2']:
                    if col in df.columns:
                        l = get_link(row[col])
                        if l: st.image(l, width=600)
                
                if 'video' in df.columns and str(row['video']).startswith('http'):
                    st.video(row['video'])
                st.divider()

except Exception as e:
    st.error("Erreur de chargement de l'onglet. Vérifiez le nom dans le Google Sheet.")

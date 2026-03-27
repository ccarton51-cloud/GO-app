import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuration
st.set_page_config(page_title="Coach Grand Oral", layout="wide")

# Fonction pour nettoyer les liens
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

# --- VIDAGE DU CACHE ET CHARGEMENT ---
@st.cache_data(ttl=10) # Force la mise à jour toutes les 10 secondes
def load_data(onglet):
    url = BASE_URL + urllib.parse.quote(onglet)
    return pd.read_csv(url).fillna("")

try:
    df = load_data(menu)
    df.columns = [c.strip().lower() for c in df.columns]

    # --- 1. SI ON EST SUR L'ETHOS ---
    if menu == "L'ETHOS":
        for i, row in df.iterrows():
            # A. NOM
            if 'nom' in df.columns and str(row['nom']).strip() not in ["", "0", "nan"]:
                st.header(row['nom'])
            
            # B. IMAGE (Colonne 'logo' dans ton Sheet Ethos)
            if 'logo' in df.columns:
                img = get_link(row['logo'])
                if img: st.image(img, width=500)
            
            # C. DESCRIPTIF
            if 'descriptif' in df.columns and str(row['descriptif']).strip() not in ["", "0", "nan"]:
                st.write(row['descriptif'])
            
            # D. EXERCICE
            if 'exercice' in df.columns and str(row['exercice']).strip() not in ["", "0", "nan"]:
                st.info(f"**L'exercice :**\n\n{row['exercice']}")
            
            st.divider()

    # --- 2. SI ON EST SUR HOME ---
    elif menu == "Home":
        st.image("https://raw.githubusercontent.com/ccarton51-cloud/GO-app/main/images/logo.png", width=200)
        st.write("Bienvenue dans ton allié ultime pour réussir le Grand Oral...")

    # --- 3. TOUTES LES AUTRES PAGES ---
    else:
        for i, row in df.iterrows():
            if 'nom' in df.columns and str(row['nom']).strip() not in ["", "0", "nan"]:
                st.header(row['nom'])
            
            if 'texte' in df.columns and str(row['texte']).strip() not in ["", "0", "nan"]:
                st.write(row['texte'])

            # Images 1 et 2
            for col in ['image 1', 'image 2']:
                if col in df.columns:
                    l = get_link(row[col])
                    if l: st.image(l, width=600)
            
            st.divider()

except Exception as e:
    st.warning(f"Chargement de l'onglet '{menu}'... Si rien n'apparaît, vérifiez le nom dans le Google Sheet.")

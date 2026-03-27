import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuration et Nettoyage du titre
st.set_page_config(page_title="Coach Grand Oral", layout="wide")

def get_link(url):
    if pd.isna(url) or len(str(url)) < 10: return None
    url = str(url).strip()
    if "github.com" in url and "raw" not in url:
        url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    return url

# 2. Connexion Sheet
SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet="

# On définit le menu (doit être EXACTEMENT comme tes onglets Sheet)
options = ["Home", "L'épreuve", "Compétences fondamentales", "ZEN", "L'ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"]
menu = st.sidebar.radio("Navigation", options)

st.title(f"Coach Grand Oral - {menu}")

# --- FONCTION DE CHARGEMENT FORCÉ ---
def load_sheet_data(onglet):
    # On ajoute un paramètre bidon à l'URL pour forcer Google à rafraîchir les données
    url = f"{BASE_URL}{urllib.parse.quote(onglet)}&cachebust={pd.Timestamp.now().timestamp()}"
    return pd.read_csv(url).fillna("")

try:
    df = load_sheet_data(menu)
    df.columns = [c.strip().lower() for c in df.columns]

    # --- LOGIQUE STRICTE PAR PAGE ---
    
    if menu == "L'ETHOS":
        # ICI ON NE CHERCHE QUE L'ETHOS
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["", "nan", "0"]:
                st.header(nom) # NOM
                
                # IMAGE (colonne 'image' d'après ta capture e65702)
                # Attention : dans ta capture, la colonne s'appelle 'image' (B)
                img_url = get_link(row.get('image', ''))
                if img_url:
                    st.image(img_url, width=500)
                
                # DESCRIPTIF
                desc = str(row.get('descriptif', '')).strip()
                if desc and desc.lower() not in ["", "nan", "0"]:
                    st.write(desc)
                
                # EXERCICE
                exo = str(row.get('exercice', '')).strip()
                if exo and exo.lower() not in ["", "nan", "0"]:
                    st.info(f"**L'exercice :**\n\n{exo}")
                
                st.divider()

    elif menu == "Home":
        st.image("https://raw.githubusercontent.com/ccarton51-cloud/GO-app/main/images/logo.png", width=200)
        st.write("Bienvenue sur votre espace de préparation au Grand Oral.")

    else:
        # AUTRES PAGES (ZEN, Epreuve...)
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["", "nan", "0"]:
                st.header(nom)
                
                txt = str(row.get('texte', '')).strip()
                if txt: st.markdown(f"### {txt}")
                
                for c in ['image', 'image 1', 'image 2']:
                    l = get_link(row.get(c, ''))
                    if l: st.image(l, width=600)
                
                if 'video' in df.columns and str(row['video']).startswith('http'):
                    st.video(row['video'])
                st.divider()

except Exception as e:
    st.error(f"Erreur lors de la lecture de l'onglet '{menu}'.")

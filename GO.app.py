import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuration
LOGO_FIXE = "https://raw.githubusercontent.com/ccarton51-cloud/GO-app/main/images/logo.png"
st.set_page_config(page_title="Coach Grand Oral", page_icon=LOGO_FIXE, layout="wide")

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
    ["Home", "L'épreuve", "Compétences fondamentales", "ZEN", "L'ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

try:
    onglet_encode = urllib.parse.quote(menu)
    df = pd.read_csv(BASE_URL + onglet_encode).fillna("")
    df.columns = [c.strip().lower() for c in df.columns]

    # --- PAGE ACCUEIL (HOME) ---
    if menu == "Home":
        st.image(LOGO_FIXE, width=200)
        st.markdown("Bienvenue dans ton allié ultime pour réussir le Grand Oral...")

    # --- PAGE L'ETHOS (Ordre spécifique demandé) ---
    elif menu == "L'ETHOS":
        for i, row in df.iterrows():
            # 1. NOM
            if 'nom' in df.columns and str(row['nom']).strip() not in ["", "0", "nan"]:
                st.header(row['nom'])
            
            # 2. IMAGE (Colonne 'logo' dans ton Sheet)
            if 'logo' in df.columns:
                img = get_link(row['logo'])
                if img:
                    st.image(img, width=600)
            
            # 3. DESCRIPTIF
            if 'descriptif' in df.columns and str(row['descriptif']).strip() not in ["", "0", "nan"]:
                st.write(f"**Note :** {row['descriptif']}")
            
            # 4. EXERCICE
            if 'exercice' in df.columns and str(row['exercice']).strip() not in ["", "0", "nan"]:
                st.info(f"**L'exercice :** \n\n {row['exercice']}")

            st.divider()

    # --- AUTRES PAGES (ZEN, L'épreuve, etc.) ---
    else:
        for i, row in df.iterrows():
            if 'nom' in df.columns and str(row['nom']).strip() not in ["", "0", "nan"]:
                st.header(row['nom'])
            
            if 'texte' in df.columns and str(row['texte']).strip() not in ["", "0", "nan"]:
                st.markdown(f"### {row['texte']}")

            for col_img in ['image 1', 'image 2']:
                if col_img in df.columns:
                    l = get_link(row[col_img])
                    if l: st.image(l, width=600)

            if 'video' in df.columns and str(row['video']).strip().startswith('http'):
                st.video(row['video'])
            
            st.divider()

except Exception as e:
    st.info("Chargement du contenu...")

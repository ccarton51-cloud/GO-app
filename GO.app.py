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

# 2. Connexion Google Sheet
SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet="

st.title("Coach Grand Oral")

# 3. Menu (Vérifie bien que les noms ici sont EXACTEMENT ceux de tes onglets Sheet)
menu = st.sidebar.radio("Navigation", 
    ["Home", "L'épreuve", "Compétences fondamentales", "ZEN", "L'ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

try:
    onglet_encode = urllib.parse.quote(menu)
    df = pd.read_csv(BASE_URL + onglet_encode).fillna("")
    df.columns = [c.strip().lower() for c in df.columns]

    # --- CAS 1 : PAGE HOME ---
    if menu == "Home":
        st.image(LOGO_FIXE, width=200)
        st.markdown("""
        Bienvenue dans ton allié ultime pour réussir le Grand Oral.  
        Cette application a été conçue comme un véritable aide-mémoire... [Ton texte complet]
        """)

    # --- CAS 2 : PAGE L'ETHOS (Structure spécifique avec Descriptif et Exercice) ---
    elif menu == "L'ETHOS":
        for i, row in df.iterrows():
            if str(row.get('nom', '')).strip() not in ["", "0", "nan"]:
                st.header(row['nom'])
            
            # Affichage du descriptif (en italique pour différencier)
            if 'descriptif' in df.columns and str(row['descriptif']).strip() not in ["", "0", "nan"]:
                st.write(f"*{row['descriptif']}*")
            
            # Affichage de l'exercice dans un encadré
            if 'exercice' in df.columns and str(row['exercice']).strip() not in ["", "0", "nan"]:
                st.info(row['exercice'])

            # Image de l'exercice (colonne 'logo')
            if 'logo' in df.columns:
                img = get_link(row['logo'])
                if img:
                    st.image(img, width=600)
            st.divider()

    # --- CAS 3 : TOUTES LES AUTRES PAGES (ZEN, L'épreuve, etc.) ---
    else:
        for i, row in df.iterrows():
            if 'nom' in df.columns and str(row['nom']).strip() not in ["", "0", "nan"]:
                st.header(row['nom'])
            
            if 'texte' in df.columns and str(row['texte']).strip() not in ["", "0", "nan"]:
                # On agrandit un peu le texte pour ZEN comme demandé
                st.markdown(f"### {row['texte']}")

            # Images 1 et 2
            for col_img in ['image 1', 'image 2']:
                if col_img in df.columns:
                    l = get_link(row[col_img])
                    if l: st.image(l, width=600)

            if 'video' in df.columns and str(row['video']).strip().startswith('http'):
                st.video(row['video'])
            
            st.divider()

except Exception as e:
    st.error(f"Erreur : Vérifie que l'onglet '{menu}' existe dans ton Sheet avec les bonnes colonnes.")

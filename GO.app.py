import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuration de la page
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

# 3. Navigation (Mise à jour avec ton nouveau nom d'onglet)
menu = st.sidebar.radio("Navigation", 
    ["Home", "L'épreuve", "Compétences fondamentales", "ZEN", "L'ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

# --- CHARGEMENT DYNAMIQUE ---
try:
    onglet_encode = urllib.parse.quote(menu)
    df = pd.read_csv(BASE_URL + onglet_encode).fillna("")
    df.columns = [c.strip().lower() for c in df.columns]

    # --- PAGE ACCUEIL (HOME) ---
    if menu == "Home":
        img_url = LOGO_FIXE
        if 'logo' in df.columns:
            link = get_link(df['logo'].iloc[0])
            if link: img_url = link
        st.image(img_url, width=200)
        st.markdown("""Bienvenue dans ton allié ultime pour réussir le Grand Oral...""") # Ton texte de bienvenue

    # --- PAGES DE CONTENU (ZEN, ETHOS, etc.) ---
    else:
        for i, row in df.iterrows():
            # A. Titre de l'exercice (Colonne 'Nom')
            nom = str(row.get('nom', '')).strip()
            if nom and nom not in ["0", "nan"]:
                st.header(nom)
            
            # B. Descriptif ou Texte principal
            # On cherche soit 'descriptif' (ETHOS) soit 'texte' (ZEN)
            txt_principal = str(row.get('descriptif', row.get('texte', ''))).strip()
            if txt_principal and txt_principal not in ["0", "nan"]:
                st.subheader(txt_principal)

            # C. L'Exercice détaillé (Spécifique à ETHOS)
            exercice = str(row.get('exercice', '')).strip()
            if exercice and exercice not in ["0", "nan"]:
                st.info(exercice) # Mis en évidence dans un encadré bleu

            # D. Images (On cherche 'logo', 'image 1', 'image 2')
            # Dans ETHOS, tes images sont dans la colonne 'logo'
            liens_valides = []
            for col_img in ['logo', 'image 1', 'image 2', 'image']:
                # On évite d'afficher le logo de la Home sur les autres pages
                if menu != "Home" or col_img != "logo":
                    l = get_link(row.get(col_img, ''))
                    if l: liens_valides.append(l)
            
            for l in liens_valides:
                st.image(l, width=600)

            # E. Vidéo
            if 'video' in df.columns and str(row['video']).startswith('http'):
                st.video(row['video'])
            
            st.divider()

except Exception as e:
    st.info("Sélectionnez une section dans le menu de gauche.")

import streamlit as st
import pandas as pd
import re
import urllib.parse

# 1. Configuration de la page
LOGO_GITHUB = "https://raw.githubusercontent.com/ccarton51-cloud/GO-app/main/images/logo.png"
st.set_page_config(page_title="Coach Grand Oral", page_icon=LOGO_GITHUB, layout="wide")

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

# Titre visible sur toutes les pages
st.title("Coach Grand Oral")

# 3. Navigation
menu = st.sidebar.radio("Navigation", 
    ["Home", "L'épreuve", "Compétences fondamentales", "ZEN", "Exercices ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

# --- PAGE ACCUEIL (HOME) ---
if menu == "Home":
    # On essaie de charger l'image depuis la colonne 'logo' du Sheet
    image_a_afficher = LOGO_GITHUB # Par défaut
    
    try:
        df_home = pd.read_csv(BASE_URL + "Home").fillna("")
        df_home.columns = [c.strip().lower() for c in df_home.columns]
        
        if 'logo' in df_home.columns:
            link = get_link(df_home['logo'].iloc[0])
            if link:
                image_a_afficher = link
    except:
        pass # On garde le LOGO_GITHUB par défaut en cas d'erreur
    
    st.image(image_a_afficher, width=200)

    st.markdown("""
    Bienvenue dans ton allié ultime pour réussir le Grand Oral.  
    Cette application a été conçue comme un véritable aide-mémoire, simple et efficace, pour t’accompagner partout dans ta préparation. Tu y trouveras tout l’essentiel pour aborder l’épreuve avec confiance : le déroulement détaillé du Grand Oral pour savoir exactement à quoi t’attendre, des “plans zen” pour apprendre à gérer ton stress et rester serein, ainsi que des exercices pratiques pour maîtriser les fondamentaux de la prise de parole — ethos, pathos, logos — et faire passer ton message avec impact.  
    
    Pour profiter pleinement de toutes ces ressources, utilise la navigation de l’application afin d’accéder facilement aux différentes sections et avancer à ton rythme.  
    
    Parce que la réussite se construit aussi dans les derniers jours, un compte à rebours t’accompagne de J-7 jusqu’au jour J, avec des rappels et des conseils pour rester concentré et prêt au bon moment.  
    
    Que tu sois en train de commencer tes révisions ou dans la dernière ligne droite, cette application est là pour te guider, t’entraîner et te rassurer. À toi de jouer.
    """)

# --- AUTRES PAGES ---
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

            # Images 1 et 2 uniquement
            liens_valides = []
            for col_img in ['image 1', 'image 2']:
                if col_img in df.columns:
                    l = get_link(row[col_img])
                    if l: liens_valides.append(l)
            
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
        st.info("Sélectionnez une section dans le menu.")

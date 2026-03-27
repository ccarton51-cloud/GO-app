import streamlit as st
import pandas as pd
import re

# 1. Configuration de la page (Favicon Chrome)
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

# --- TITRE SANS ÉMOJI (Visible sur toutes les pages) ---
st.title("Coach Grand Oral")

# 3. Navigation
menu = st.sidebar.radio("Navigation", 
    ["Home", "L'épreuve", "Compétences fondamentales", "ZEN", "Exercices ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

# --- PAGE ACCUEIL (HOME) ---
if menu == "Home":
    # Affichage du logo sous le titre
    st.image(LOGO_URL, width=200)

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
        # On nettoie le nom pour l'URL (gestion de l'apostrophe et des accents)
        import urllib.parse
        onglet_encode = urllib.parse.quote(menu)
        
        # Chargement des données
        df = pd.read_csv(BASE_URL + onglet_encode).fillna("")
        df.columns = [c.strip().lower() for c in df.columns]

        if df.empty:
            st.warning(f"L'onglet '{menu}' semble vide ou n'existe pas dans le Google Sheet.")
        else:
            for i, row in df.iterrows():
                # On affiche le titre s'il existe
                nom_col = 'nom' if 'nom' in df.columns else None
                if nom_col and str(row[nom_col]).strip() not in ["", "0", "nan"]:
                    st.header(row[nom_col])
                
                # Texte principal
                if 'texte' in df.columns and str(row['texte']).strip() not in ["", "0", "nan"]:
                    st.write(row['texte'])

                # Gestion des images (image 1, image 2, etc.)
                cols_img = [c for c in df.columns if 'image' in c]
                liens_valides = [get_link(row[c]) for c in cols_img if get_link(row[c])]
                
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
                
                # Textes secondaires
                for c in df.columns:
                    if 'texte' in c and c != 'texte':
                        val = str(row[c]).strip()
                        if val and val not in ["", "0", "nan"]:
                            st.write(val)
                st.divider()

    except Exception as e:
        st.error(f"Impossible de charger l'onglet '{menu}'. Vérifiez qu'il existe bien dans votre Google Sheet.")
        st.info("Astuce : Vérifiez que le nom de l'onglet en bas de votre Excel est exactement 'L'épreuve'")

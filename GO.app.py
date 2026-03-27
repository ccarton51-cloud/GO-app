import streamlit as st
import pandas as pd
import urllib.parse
import time

# 1. Configuration de la page
st.set_page_config(page_title="Coach Grand Oral", layout="wide")

# Fonction de nettoyage des liens ultra-robuste
def get_clean_link(url):
    if pd.isna(url) or len(str(url)) < 10: return None
    url = str(url).strip()
    if "github.com" in url and "raw=true" not in url and "raw.githubusercontent.com" not in url:
        if "/blob/" in url:
            url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        else:
            if "?" in url: url = url.split("?")[0]
            url = url + "?raw=true"
    return url

# 2. Paramètres Google Sheet
SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"

TABS = {
    "Home": "Home",
    "L'épreuve": "L'épreuve",
    "Compétences fondamentales": "Compétences fondamentales",
    "ZEN": "ZEN",
    "L'ETHOS": "434742742", 
    "Exercices LOGOS": "Exercices LOGOS",
    "Exercices PATHOS": "Exercices PATHOS",
    "Countdown": "Countdown"
}

menu = st.sidebar.radio("Navigation", list(TABS.keys()))
st.title(f"Coach Grand Oral")

try:
    target = TABS[menu]
    if target.isdigit():
        url_base = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={target}"
    else:
        url_base = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(target)}"
    
    timestamp = int(time.time())
    full_url = f"{url_base}&cachebuster={timestamp}"
    df = pd.read_csv(full_url).fillna("")
    df.columns = [c.strip().lower() for c in df.columns]

    # --- AFFICHAGE HOME (Logo réduit) ---
    if menu == "Home":
        # Taille réduite à 200px pour le logo d'accueil
        st.image("https://raw.githubusercontent.com/ccarton51-cloud/GO-app/main/images/logo.png", width=200)
        
        st.markdown("""
        Bienvenue dans ton allié ultime pour réussir le Grand Oral.  
        Cette application a été conçue comme un véritable aide-mémoire, simple et efficace, pour t’accompagner partout dans ta préparation. Tu y trouveras tout l’essentiel pour aborder l’épreuve avec confiance : le déroulement détaillé du Grand Oral pour savoir exactement à quoi t’attendre, des “plans zen” pour apprendre à gérer ton stress et rester serein, ainsi que des exercices pratiques pour maîtriser les fondamentaux de la prise de parole — ethos, pathos, logos — et faire passer ton message avec impact.  
        
        Pour profiter pleinement de toutes

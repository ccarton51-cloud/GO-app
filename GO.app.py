import streamlit as st
import pandas as pd
import urllib.parse
import time

# 1. Configuration de la page
st.set_page_config(page_title="Coach Grand Oral", layout="wide")

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

# --- CONFIGURATION DES ONGLETS ---
TABS = {
    "Home": "Home",
    "L'épreuve": "L'épreuve",
    "Compétences fondamentales": "Compétences fondamentales",
    "ZEN": "ZEN",
    "L'ETHOS": "434742742", 
    "LOGOS": "LOGOS",
    "PATHOS": "PATHOS", # Ajouté ici
    "Countdown": "Countdown"
}

menu = st.sidebar.radio("Navigation", list(TABS.keys()))
st.title(f"Coach Grand Oral")

try:
    target = TABS[menu]
    # Si c'est un chiffre (GID), on utilise l'export direct, sinon le nom d'onglet
    if target.isdigit():
        url_base = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={target}"
    else:
        url_base = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(target)}"
    
    # Force le rafraîchissement
    timestamp = int(time.time())
    full_url = f"{url_base}&cachebuster={timestamp}"
    df = pd.read_csv(full_url).fillna("")
    df.columns = [c.strip().lower() for c in df.columns]

    # --- LOGIQUE POUR ETHOS, LOGOS ET PATHOS (Structure fixe + Images 400px) ---
    if menu in ["L'ETHOS", "LOGOS", "PATHOS"]:
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.header(nom) # 1. NOM
                
                # 2. IMAGE (Largeur contrôlée à 400px)
                img_val = row.get('image', row.get('logo', ''))
                img_url = get_clean_link(img_val)
                if img_url:
                    st.image(img_url, width=400)
                
                # 3. DESCRIPTIF / TEXTE
                desc = str(row.get('descriptif', row.get('texte', ''))).strip()
                if desc and desc.lower() not in ["nan", "0", ""]:
                    st.markdown(desc)
                
                # 4. EXERCICE (Bloc info bleu)
                exo = str(row.get('exercice', '')).strip()
                if exo and exo.lower() not in ["nan", "0", ""]:
                    st.info(f"**L'exercice :**\n\n{exo}")
                
                st.divider()

    # --- AFFICHAGE HOME ---
    elif menu == "Home":
        st.image("https://raw.githubusercontent.com/ccarton51-cloud/GO-app/main/images/logo.png", width=200)
        st.markdown("""
        Bienvenue dans ton allié ultime pour réussir le Grand Oral.  
        Cette application a été conçue comme un véritable aide-mémoire pour t’accompagner partout dans ta préparation. 
        
        Utilise la navigation pour accéder aux différentes sections : le déroulement de l'épreuve, les conseils ZEN, 
        et les exercices pour maîtriser l'**Ethos**, le **Logos** et le **Pathos**.
        """)

    # --- AUTRES PAGES (ZEN, Épreuve...) ---
    else:
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower()

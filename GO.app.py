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

# Mise à jour des noms d'onglets (LOGOS au lieu de Exercices LOGOS)
TABS = {
    "Home": "Home",
    "L'épreuve": "L'épreuve",
    "Compétences fondamentales": "Compétences fondamentales",
    "ZEN": "ZEN",
    "L'ETHOS": "434742742", 
    "LOGOS": "LOGOS", # Changement de nom ici
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

    # --- LOGIQUE POUR L'ETHOS ET LE LOGOS (Images à 400px) ---
    if menu in ["L'ETHOS", "LOGOS"]:
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.header(nom)
                
                # Image réduite à 400px
                img_val = row.get('image', row.get('logo', ''))
                img_url = get_clean_link(img_val)
                if img_url:
                    st.image(img_url, width=400)
                
                # Descriptif / Texte
                desc = str(row.get('descriptif', row.get('texte', ''))).strip()
                if desc and desc.lower() not in ["nan", "0", ""]:
                    st.markdown(desc)
                
                # Exercice
                exo = str(row.get('exercice', '')).strip()
                if exo and exo.lower() not in ["nan", "0", ""]:
                    st.info(f"**L'exercice :**\n\n{exo}")
                st.divider()

    # --- AFFICHAGE HOME ---
    elif menu == "Home":
        st.image("https://raw.githubusercontent.com/ccarton51-cloud/GO-app/main/images/logo.png", width=200)
        st.markdown("""
        Bienvenue dans ton allié ultime pour réussir le Grand Oral... 
        *(Texte complet de bienvenue)*
        """)

    # --- AUTRES PAGES ---
    else:
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.header(nom)
                txt = str(row.get('texte', '')).strip()
                if txt: st.markdown(f"### {txt}")
                
                image_cols = [c for c in df.columns if 'image' in c or 'logo' in c]
                for c in image_cols:
                    l = get_clean_link(row[c])
                    if l: st.image(l, use_container_width=True)
                
                if 'video' in df.columns and str(row['video']).startswith('http'):
                    st.video(row['video'])
                st.divider()

except Exception as e:
    st.error(f"Erreur : {e}")

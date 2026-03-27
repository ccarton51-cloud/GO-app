import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuration
st.set_page_config(page_title="Coach Grand Oral", layout="wide")

def get_link(url):
    if pd.isna(url) or len(str(url)) < 10: return None
    url = str(url).strip()
    if "github.com" in url and "raw" not in url:
        url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    if "?" in url: url = url.split("?")[0] # Nettoyage des paramètres
    return url

# 2. Paramètres Google Sheet
SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"

# --- CONFIGURATION DES ONGLETS ---
# Si un onglet bugge, remplace son nom par son GID (ex: "ZEN": "123456")
TABS = {
    "Home": "0",
    "L'épreuve": "L'épreuve",
    "Compétences fondamentales": "Compétences fondamentales",
    "ZEN": "ZEN",
    "L'ETHOS": "434742742",  # Ton GID tout neuf !
    "Exercices LOGOS": "Exercices LOGOS",
    "Exercices PATHOS": "Exercices PATHOS",
    "Countdown": "Countdown"
}

menu = st.sidebar.radio("Navigation", list(TABS.keys()))
st.title(f"Coach Grand Oral")

# --- CHARGEMENT DES DONNÉES ---
try:
    target = TABS[menu]
    # Si la cible est un chiffre (GID), on utilise l'export par GID, sinon par nom d'onglet
    if target.isdigit():
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={target}"
    else:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(target)}"
    
    # On force le rafraîchissement avec un timestamp
    df = pd.read_csv(f"{url}&cache={pd.Timestamp.now().timestamp()}").fillna("")
    
    # Nettoyage standard des noms de colonnes (Minuscules et sans espaces)
    df.columns = [c.strip().lower() for c in df.columns]

    # --- AFFICHAGE L'ETHOS ---
    if menu == "L'ETHOS":
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.header(nom) # 1. NOM
                
                # 2. IMAGE (colonne 'image' ou 'logo')
                img_val = row.get('image', row.get('logo', ''))
                img_url = get_link(img_val)
                if img_url:
                    st.image(img_url, width=500)
                
                # 3. DESCRIPTIF
                desc = str(row.get('descriptif', '')).strip()
                if desc and desc.lower() not in ["nan", "0", ""]:
                    st.write(desc)
                
                # 4. EXERCICE
                exo = str(row.get('exercice', '')).strip()
                if exo and exo.lower() not in ["nan", "0", ""]:
                    st.info(f"**L'exercice :**\n\n{exo}")
                
                st.divider()

    # --- AFFICHAGE HOME ---
    elif menu == "Home":
        st.image("https://raw.githubusercontent.com/ccarton51-cloud/GO-app/main/images/logo.png", width=200)
        st.write("Bienvenue sur votre espace de préparation au Grand Oral.")

    # --- AFFICHAGE AUTRES PAGES ---
    else:
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.header(nom)
                
                txt = str(row.get('texte', '')).strip()
                if txt: st.markdown(f"### {txt}")
                
                for c in ['image', 'image 1', 'image 2']:
                    if c in df.columns:
                        l = get_link(row[c])
                        if l: st.image(l, width=600)
                
                if 'video' in df.columns and str(row['video']).startswith('http'):
                    st.video(row['video'])
                st.divider()

except Exception as e:
    st.error(f"Erreur d'accès à l'onglet : {e}")

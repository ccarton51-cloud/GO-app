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
    
    # Force la conversion GitHub vers format RAW s'il manque le paramètre
    if "github.com" in url and "raw=true" not in url and "raw.githubusercontent.com" not in url:
        if "/blob/" in url:
            url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        else:
            # Ajoute ?raw=true si c'est un lien github standard
            if "?" in url: url = url.split("?")[0]
            url = url + "?raw=true"
    
    # Si le lien finit déjà par ?raw=true, on le garde
    return url

# 2. Paramètres Google Sheet
SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"

# --- CONFIGURATION DES ONGLETS ---
# On utilise le GID pour L'ETHOS pour être précis. Les autres par nom.
TABS = {
    "Home": "Home",
    "L'épreuve": "L'épreuve",
    "Compétences fondamentales": "Compétences fondamentales",
    "ZEN": "ZEN",
    "L'ETHOS": "434742742", # Ton GID cible
    "Exercices LOGOS": "Exercices LOGOS",
    "Exercices PATHOS": "Exercices PATHOS",
    "Countdown": "Countdown"
}

menu = st.sidebar.radio("Navigation", list(TABS.keys()))
st.title(f"Coach Grand Oral")

# --- CHARGEMENT DES DONNÉES SANS CACHE ---
try:
    target = TABS[menu]
    # Construction de l'URL d'export
    if target.isdigit():
        url_base = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={target}"
    else:
        url_base = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(target)}"
    
    # Force le rafraîchissement avec un timestamp unique à chaque seconde
    timestamp = int(time.time())
    full_url = f"{url_base}&cachebuster={timestamp}"
    
    # Lecture des données
    df = pd.read_csv(full_url).fillna("")
    
    # Nettoyage des noms de colonnes (Minuscules, pas d'espaces)
    df.columns = [c.strip().lower() for c in df.columns]

    # --- AFFICHAGE L'ETHOS (Logique Spécifique GID) ---
    if menu == "L'ETHOS":
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            # On n'affiche que les lignes avec un vrai nom
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.header(nom) # 1. NOM
                
                # 2. IMAGE (colonne B, maintenant appelée 'image' ou 'logo')
                img_val = row.get('image', row.get('logo', ''))
                img_url = get_clean_link(img_val)
                if img_url:
                    # MODIFICATION ICI : On utilise une largeur fixe (width=400)
                    # et on enlève use_container_width=True
                    st.image(img_url, width=400)
                
                # 3. DESCRIPTIF
                desc = str(row.get('descriptif', '')).strip()
                if desc and desc.lower() not in ["nan", "0", ""]:
                    st.markdown(desc)
                
                # 4. EXERCICE
                exo = str(row.get('exercice', '')).strip()
                if exo and exo.lower() not in ["nan", "0", ""]:
                    st.info(f"**L'exercice :**\n\n{exo}")
                
                st.divider()

    # --- AFFICHAGE ZEN ET AUTRES PAGES (Méthode standard) ---
    else:
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.header(nom)
                
                txt = str(row.get('texte', '')).strip()
                if txt and txt.lower() not in ["nan", "0", ""]:
                    # On affiche le texte un peu plus gros pour ZEN
                    st.markdown(f"### {txt}")
                
                # Cherche n'importe quelle colonne image valide (image, logo, image 1, etc.)
                image_cols = [c for c in df.columns if 'image' in c or 'logo' in c]
                for c in image_cols:
                    l = get_clean_link(row[c])
                    if l: 
                        st.image(l, use_container_width=True)
                
                # Vidéo
                if 'video' in df.columns and str(row['video']).startswith('http'):
                    st.video(row['video'])
                st.divider()

except Exception as e:
    st.error(f"Impossible de charger le contenu de l'onglet '{menu}'. Erreur : {e}")

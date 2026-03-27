import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Coach Grand Oral", page_icon="🎓", layout="wide")

def get_link(url):
    # Sécurité absolue : si c'est pas du texte ou si c'est trop court, on ignore
    if pd.isna(url) or len(str(url)) < 10: 
        return None
    
    url = str(url).strip()
    
    # SI LE LIEN NE COMMENCE PAS PAR HTTP, ON L'IGNORE (bye bye les "0")
    if not url.lower().startswith('http'):
        return None

    # Conversion GitHub Raw
    if "github.com" in url and "raw" not in url:
        url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    
    return url

SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet="

st.title("🎓 Coach Grand Oral")
menu = st.sidebar.radio("Navigation", ["Home", "Compétences fondamentales", "ZEN", "Exercices ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

try:
    onglet_nom = menu.replace(" ", "%20")
    df = pd.read_csv(BASE_URL + onglet_nom).fillna("")
    df.columns = [c.strip().lower() for c in df.columns]

    for i, row in df.iterrows():
        # Titre section
        nom = str(row.get('nom', '')).strip()
        if nom and nom not in ["0", "nan"]:
            st.header(nom)
        
        # Texte principal
        txt = str(row.get('texte', '')).strip()
        if txt and txt not in ["0", "nan"]:
            st.write(txt)

        # GESTION DES IMAGES (Colonnes image 1, image 2, etc.)
        # On ne cherche que les colonnes qui contiennent "image"
        cols_img = [c for c in df.columns if 'image' in c]
        liens_valides = []
        
        for c in cols_img:
            link = get_link(row[c])
            if link:
                liens_valides.append(link)
        
        # Affichage des images trouvées
        if liens_valides:
            if len(liens_valides) > 1:
                cols = st.columns(len(liens_valides))
                for idx, l in enumerate(liens_valides):
                    cols[idx].image(l, use_container_width=True)
            else:
                st.image(liens_valides[0], use_container_width=True)

        # Vidéo
        if 'video' in df.columns:
            v = str(row['video']).strip()
            if v.startswith('http'):
                st.video(v)
            
        # Textes secondaires
        for c in df.columns:
            if 'texte' in c and c != 'texte':
                val = str(row[c]).strip()
                if val and val not in ["0", "nan"]:
                    st.write(val)
        
        st.divider()

except Exception as e:
    st.error("Mise à jour du contenu...")

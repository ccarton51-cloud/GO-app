import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Coach Grand Oral", page_icon="🎓", layout="wide")

def get_link(url):
    # On ignore le lien si c'est vide, nan, ou juste un "0"
    if pd.isna(url) or str(url).strip() in ["", "0", "nan", "0.0"]: 
        return None
    url = str(url).strip()
    if "github.com" in url and "raw" not in url:
        url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    if "drive.google.com" in url:
        file_id = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
        if file_id: return f"https://drive.google.com/uc?export=view&id={file_id.group(1)}"
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
        # 1. Titre
        nom_section = str(row.get('nom', '')).strip()
        if nom_section and nom_section not in ["", "0", "nan"]:
            st.header(nom_section)
        
        # 2. Texte Principal
        texte_p = str(row.get('texte', '')).strip()
        if texte_p and texte_p not in ["", "0", "nan"]:
            st.write(texte_p)

        # 3. IMAGES (Gestion image 1, image 2, etc.)
        # On récupère toutes les colonnes qui contiennent "image"
        cols_img = [c for c in df.columns if 'image' in c]
        liens_valides = []
        for c in cols_img:
            link = get_link(row[c])
            if link: liens_valides.append(link)
        
        if liens_valides:
            if len(liens_valides) > 1:
                st_cols = st.columns(len(liens_valides))
                for idx, link in enumerate(liens_valides):
                    st_cols[idx].image(link, use_container_width=True)
            else:
                st.image(liens_valides[0], use_container_width=True)

        # 4. Vidéo
        if 'video' in df.columns:
            v_link = str(row['video']).strip()
            if v_link and v_link not in ["", "0", "nan"]:
                st.video(v_link)
            
        # 5. Textes additionnels (texte1, texte2, etc.)
        for c in df.columns:
            if ('texte' in c and c != 'texte'):
                val = str(row[c]).strip()
                if val and val not in ["", "0", "nan"]:
                    st.write(val)
        
        st.divider()

except Exception as e:
    st.error(f"Mise à jour en cours...")

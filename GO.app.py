import streamlit as st
import pandas as pd
import urllib.parse
import time

st.set_page_config(page_title="Coach Grand Oral", layout="wide")

def get_clean_link(url):
    # On élimine les "0", les "nan" et les textes vides qui font planter l'affichage
    if pd.isna(url) or str(url).strip() in ["", "0", "nan", "None"]: 
        return None
    url = str(url).strip()
    if "github.com" in url and "raw=true" not in url and "raw.githubusercontent.com" not in url:
        if "/blob/" in url:
            url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        else:
            if "?" in url: url = url.split("?")[0]
            url = url + "?raw=true"
    return url

SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"

TABS = {
    "Home": "Home",
    "L'épreuve": "L'épreuve",
    "Compétences fondamentales": "Compétences fondamentales",
    "ZEN": "ZEN",
    "L'ETHOS": "434742742", 
    "LOGOS": "LOGOS",
    "PATHOS": "PATHOS",
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
    
    # ÉTAPE CRUCIALE : On change le nom du paramètre cache à chaque seconde
    # pour forcer Google à renvoyer les toutes dernières données.
    full_url = f"{url_base}&t={int(time.time())}"
    
    df = pd.read_csv(full_url).fillna("")
    df.columns = [c.strip().lower() for c in df.columns]

    if menu == "Home":
        st.image("https://raw.githubusercontent.com/ccarton51-cloud/GO-app/main/images/logo.png", width=200)
        st.write("Bienvenue dans ton allié ultime pour réussir le Grand Oral.")

    elif menu in ["L'ETHOS", "LOGOS", "PATHOS"]:
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.header(nom)
                img_url = get_clean_link(row.get('image', row.get('logo', '')))
                if img_url: st.image(img_url, width=400)
                desc = str(row.get('descriptif', row.get('texte', ''))).strip()
                if desc and desc not in ["0", "nan"]: st.write(desc)
                exo = str(row.get('exercice', '')).strip()
                if exo and exo not in ["0", "nan"]: st.info(f"**L'exercice :**\n\n{exo}")
                st.divider()

    else:
        # Logique pour L'épreuve, ZEN, etc.
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.header(nom)
                
                # Textes
                for col in [c for c in df.columns if 'texte' in c]:
                    t = str(row[col]).strip()
                    if t and t.lower() not in ["nan", "0", ""]:
                        st.write(t)
                
                # Images (Scanne TOUTES les colonnes contenant "image" ou "logo")
                img_cols = [c for c in df.columns if 'image' in c or 'logo' in c]
                for col in img_cols:
                    valeur_cellule = row[col]
                    l = get_clean_link(valeur_cellule)
                    if l:
                        st.image(l, use_container_width=True)
                
                st.divider()

except Exception as e:
    st.error(f"Erreur : {e}")

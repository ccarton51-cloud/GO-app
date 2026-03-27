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

    # --- AFFICHAGE HOME ---
    if menu == "Home":
        st.image("https://raw.githubusercontent.com/ccarton51-cloud/GO-app/main/images/logo.png", width=200)
        st.markdown("""
        Bienvenue dans ton allié ultime pour réussir le Grand Oral.  
        Cette application a été conçue comme un véritable aide-mémoire, simple et efficace, pour t’accompagner partout dans ta préparation. Tu y trouveras tout l’essentiel pour aborder l’épreuve avec confiance : le déroulement détaillé du Grand Oral pour savoir exactement à quoi t’attendre, des “plans zen” pour apprendre à gérer ton stress et rester serein, ainsi que des exercices pratiques pour maîtriser les fondamentaux de la prise de parole — ethos, pathos, logos — et faire passer ton message avec impact.  
        
        Pour profiter pleinement de toutes ces ressources, utilise la navigation de l’application afin d’accéder facilement aux différentes sections et avancer à ton rythme.  
        
        Parce que la réussite se construit aussi dans les derniers jours, un compte à rebours t’accompagne de J-7 jusqu’au jour J, avec des rappels et des conseils pour rester concentré et prêt au bon moment.  
        
        Que tu sois en train de commencer tes révisions ou dans la dernière ligne droite, cette application est là pour te guider, t’entraîner et te rassurer. À toi de jouer.
        """) # <--- Les guillemets sont bien fermés ici !

    # --- AFFICHAGE L'ETHOS ---
    elif menu == "L'ETHOS":
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.header(nom)
                img_val = row.get('image', row.get('logo', ''))
                img_url = get_clean_link(img_val)
                if img_url:
                    st.image(img_url, width=400)
                
                desc = str(row.get('descriptif', '')).strip()
                if desc and desc.lower() not in ["nan", "0", ""]:
                    st.markdown(desc)
                
                exo = str(row.get('exercice', '')).strip()
                if exo and exo.lower() not in ["nan", "0", ""]:
                    st.info(f"**L'exercice :**\n\n{exo}")
                st.divider()

    # --- AFFICHAGE AUTRES PAGES ---
    else:
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.header(nom)
                txt = str(row.get('texte', '')).strip()
                if txt and txt.lower() not in ["nan", "0", ""]:
                    st.markdown(f"### {txt}")
                
                image_cols = [c for c in df.columns if 'image' in c or 'logo' in c]
                for c in image_cols:
                    l = get_clean_link(row[c])
                    if l: 
                        st.image(l, use_container_width=True)
                
                if 'video' in df.columns and str(row['video']).startswith('http'):
                    st.video(row['video'])
                st.divider()

except Exception as e:
    st.error(f"Erreur : {e}")

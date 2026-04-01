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

# --- CONFIGURATION DES ONGLETS (Compétences fondamentales supprimé) ---
TABS = {
    "Home": "Home",
    "L'épreuve": "L'épreuve",
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
    
    timestamp = int(time.time())
    full_url = f"{url_base}&cachebuster={timestamp}"
    df = pd.read_csv(full_url).fillna("")
    df.columns = [c.strip().lower() for c in df.columns]

    # --- 1. AFFICHAGE HOME ---
    if menu == "Home":
        st.image("https://raw.githubusercontent.com/ccarton51-cloud/GO-app/main/images/logo.png", width=200)
        st.markdown("""
        Bienvenue dans ton allié ultime pour réussir le Grand Oral.  
        Cette application a été conçue comme un véritable aide-mémoire pour t’accompagner partout dans ta préparation. 
        
        Utilise la navigation pour accéder aux différentes sections : le déroulement de l'épreuve, les conseils ZEN, 
        et les exercices pour maîtriser l'**Ethos**, le **Logos** et le **Pathos**.
        """)

    # --- 2. LOGIQUE SPÉCIFIQUE COUNTDOWN ---
    elif menu == "Countdown":
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.header(f"⏳ {nom}")
                
                img_url = get_clean_link(row.get('image', ''))
                if img_url:
                    st.image(img_url, width=500)

                col_intro1, col_intro2 = st.columns(2)
                with col_intro1:
                    desc = str(row.get('descriptif', '')).strip()
                    if desc: st.markdown(f"**Objectif :** {desc}")
                with col_intro2:
                    exo = str(row.get('exercice', '')).strip()
                    if exo: st.info(f"**Exercice de préparation :**\n\n{exo}")

                st.write("---")
                st.subheader("📋 Ton programme")
                cols_textes = st.columns(2)
                
                text_count = 0
                for i in range(1, 6):
                    col_name = f"texte {i}"
                    val = str(row.get(col_name, '')).strip()
                    if val and val.lower() not in ["nan", ""]:
                        with cols_textes[text_count % 2]:
                            with st.expander(f"Étape {i}", expanded=True):
                                st.write(val)
                        text_count += 1

                st.write("---")
                c_fin1, c_fin2 = st.columns(2)
                with c_fin1:
                    cons = str(row.get('conseil', '')).strip()
                    if cons: st.warning(f"💡 **Conseil :**\n\n{cons}")
                with c_fin2:
                    det = str(row.get('détente', '')).strip()
                    if det: st.success(f"🧘 **Détente :**\n\n{det}")
                
                st.divider()

    # --- 3. LOGIQUE POUR ETHOS, LOGOS ET PATHOS ---
    elif menu in ["L'ETHOS", "LOGOS", "PATHOS"]:
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.header(nom)
                
                img_val = row.get('image', row.get('logo', ''))
                img_url = get_clean_link(img_val)
                if img_url:
                    st.image(img_url, width=400)
                
                desc = str(row.get('descriptif', row.get('texte', ''))).strip()
                if desc and desc.lower() not in ["nan", "0", ""]:
                    st.write(desc)
                
                exo = str(row.get('exercice', '')).strip()
                if exo and exo.lower() not in ["nan", "0", ""]:
                    st.info(f"**L'exercice :**\n\n{exo}")
                
                st.divider()

    # --- 4. AUTRES PAGES (ZEN, Épreuve...) ---
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
                    if l: st.image(l, use_container_width=True)
                
                if 'video' in df.columns and str(row['video']).startswith('http'):
                    st.video(row['video'])
                
                st.divider()

except Exception as e:
    st.error(f"Erreur de chargement : {e}")

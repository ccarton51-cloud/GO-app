import streamlit as st
import pandas as pd
import urllib.parse
import time

# 1. Configuration de la page
st.set_page_config(page_title="Coach Grand Oral", layout="wide")

# --- STYLE PERSONNALISÉ (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    h1 {
        color: #2c3e50 !important;
        font-family: 'Georgia', serif;
        font-weight: 700;
    }
    
    .st-expander {
        background-color: white !important;
        border-radius: 10px !important;
        border-left: 5px solid #2c3e50 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    
    .stRadio [role=radiogroup] {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

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

# --- CONFIGURATION DES ONGLETS AVEC NOUVEAUX SYMBOLES ---
TABS = {
    "Home": "Home",
    "L'épreuve": "L'épreuve",
    "ZEN": "ZEN",
    "L'ETHOS": "434742742", 
    "LOGOS": "LOGOS",
    "PATHOS": "PATHOS",
    "Countdown": "Countdown"
}

# Icônes pour la barre latérale
TAB_ICONS = {
    "Home": "🏛️",
    "L'épreuve": "📜",
    "ZEN": "🌊",
    "L'ETHOS": "🎭",
    "LOGOS": "🏛️",
    "PATHOS": "🕯️",
    "Countdown": "⚓"
}

# Création du menu avec les nouveaux icônes
menu_labels = [f"{TAB_ICONS[k]} {k}" for k in TABS.keys()]
choice = st.sidebar.radio("🧭 Orientation", menu_labels)
menu = choice.split(" ", 1)[1] # On récupère le nom sans l'icône pour la logique

st.title(f"{TAB_ICONS[menu]} {menu}")

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

    if menu == "Home":
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image("https://raw.githubusercontent.com/ccarton51-cloud/GO-app/main/images/logo.png", width=120)
        with col2:
            st.markdown("""
            ### L'art de la parole à portée de main.
            Bienvenue dans votre espace de préparation. Cet outil a été conçu pour structurer votre pensée et affiner votre éloquence.
            
            *Utilisez le menu de navigation pour explorer les piliers de votre réussite.*
            """)
        st.divider()

    elif menu == "Countdown":
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.markdown(f"### 🗓️ {nom}")
                
                img_url = get_clean_link(row.get('image', ''))
                if img_url:
                    st.image(img_url, width="stretch")

                col_intro1, col_intro2 = st.columns(2)
                with col_intro1:
                    desc = str(row.get('descriptif', '')).strip()
                    if desc: st.markdown(f"🖋️ **Note d'intention :**\n{desc}")
                with col_intro2:
                    exo = str(row.get('exercice', '')).strip()
                    if exo: st.info(f"🛠️ **Atelier préparatoire :**\n\n{exo}")

                st.markdown("#### 📑 Protocole du jour")
                cols_textes = st.columns(2)
                
                text_count = 0
                for i in range(1, 6):
                    col_name = f"texte {i}"
                    val = str(row.get(col_name, '')).strip()
                    if val and val.lower() not in ["nan", ""]:
                        with cols_textes[text_count % 2]:
                            with st.expander(f"◈ Séquence {i}", expanded=True):
                                st.write(val)
                        text_count += 1

                st.write("---")
                c_fin1, c_fin2 = st.columns(2)
                with c_fin1:
                    cons = str(row.get('conseil', '')).strip()
                    if cons: st.warning(f"⚖️ **Arbitrage du coach :**\n\n{cons}")
                with c_fin2:
                    det = str(row.get('détente', '')).strip()
                    if det: st.success(f"🍃 **Relâchement :**\n\n{det}")
                
                st.divider()

    elif menu in ["L'ETHOS", "LOGOS", "PATHOS"]:
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.header(nom)
                img_val = row.get('image', row.get('logo', ''))
                img_url = get_clean_link(img_val)
                if img_url: st.image(img_url, width=400)
                
                desc = str(row.get('descriptif', row.get('texte', ''))).strip()
                if desc: st.write(desc)
                
                exo = str(row.get('exercice', '')).strip()
                if exo: st.info(f"🔍 **Mise en pratique :**\n\n{exo}")
                st.divider()

    else:
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.header(nom)
                txt = str(row.get('texte', '')).strip()
                if txt: st.markdown(f"##### {txt}")
                
                image_cols = [c for c in df.columns if 'image' in c or 'logo' in c]
                for c in image_cols:
                    l = get_clean_link(row[c])
                    if l: st.image(l, width="stretch")
                
                if 'video' in df.columns and str(row['video']).startswith('http'):
                    st.video(row['video'])
                st.divider()

except Exception as e:
    st.error(f"Erreur de chargement : {e}")

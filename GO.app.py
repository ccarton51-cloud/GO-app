import streamlit as st
import pandas as pd
import urllib.parse
import time

# 1. Configuration de la page
st.set_page_config(page_title="Coach Grand Oral", layout="wide")

# --- STYLE PERSONNALISÉ (CSS) ---
st.markdown("""
    <style>
    /* Fond de l'application */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Style des titres */
    h1 {
        color: #1E3A8A !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Style des cartes (Expanders et Info) */
    .st-expander {
        background-color: white !important;
        border-radius: 15px !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        margin-bottom: 10px;
    }
    
    /* Boutons de la sidebar */
    .stRadio [role=radiogroup] {
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 15px;
        padding: 15px;
    }

    /* Personnalisation des blocs Info/Warning */
    .stAlert {
        border-radius: 15px !important;
        border: none !important;
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

TABS = {
    "Home": "Home",
    "L'épreuve": "L'épreuve",
    "ZEN": "ZEN",
    "L'ETHOS": "434742742", 
    "LOGOS": "LOGOS",
    "PATHOS": "PATHOS",
    "Countdown": "Countdown"
}

menu = st.sidebar.radio("🎯 Navigation", list(TABS.keys()))
st.title(f"🚀 {menu}") # Ajout d'une icône dynamique au titre

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
        col_logo, col_txt = st.columns([1, 3])
        with col_logo:
            st.image("https://raw.githubusercontent.com/ccarton51-cloud/GO-app/main/images/logo.png", width=150)
        with col_txt:
            st.markdown("""
            ### Bienvenue dans ton allié ultime pour réussir le Grand Oral.
            Cette application a été conçue comme un véritable **aide-mémoire numérique** pour t’accompagner partout. 
            
            💡 **Conseil :** Ajoute cette page à l'écran d'accueil de ton téléphone pour y accéder comme une application !
            """)
        st.info("Utilise le menu à gauche pour commencer ta préparation.")

    elif menu == "Countdown":
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.markdown(f"## ⏳ {nom}")
                
                img_url = get_clean_link(row.get('image', ''))
                if img_url:
                    # Note : j'ai mis width="stretch" comme suggéré par tes logs
                    st.image(img_url, width="stretch")

                col_intro1, col_intro2 = st.columns(2)
                with col_intro1:
                    desc = str(row.get('descriptif', '')).strip()
                    if desc: st.markdown(f"🎯 **Objectif du jour :**\n{desc}")
                with col_intro2:
                    exo = str(row.get('exercice', '')).strip()
                    if exo: st.info(f"⚡ **À faire absolument :**\n\n{exo}")

                st.markdown("### 📋 Ton programme détaillé")
                cols_textes = st.columns(2)
                
                text_count = 0
                for i in range(1, 6):
                    col_name = f"texte {i}"
                    val = str(row.get(col_name, '')).strip()
                    if val and val.lower() not in ["nan", ""]:
                        with cols_textes[text_count % 2]:
                            with st.expander(f"🔹 Étape {i}", expanded=True):
                                st.write(val)
                        text_count += 1

                st.write("---")
                c_fin1, c_fin2 = st.columns(2)
                with c_fin1:
                    cons = str(row.get('conseil', '')).strip()
                    if cons: st.warning(f"💡 **Le conseil du coach :**\n\n{cons}")
                with c_fin2:
                    det = str(row.get('détente', '')).strip()
                    if det: st.success(f"🧘 **Zen attitude :**\n\n{det}")
                
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
                if exo: st.info(f"**L'exercice :**\n\n{exo}")
                st.divider()

    else:
        # Logique pour les autres pages
        for _, row in df.iterrows():
            nom = str(row.get('nom', '')).strip()
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.header(nom)
                txt = str(row.get('texte', '')).strip()
                if txt: st.markdown(f"#### {txt}")
                
                image_cols = [c for c in df.columns if 'image' in c or 'logo' in c]
                for c in image_cols:
                    l = get_clean_link(row[c])
                    if l: st.image(l, width="stretch")
                
                if 'video' in df.columns and str(row['video']).startswith('http'):
                    st.video(row['video'])
                st.divider()

except Exception as e:
    st.error(f"Erreur de chargement : {e}")

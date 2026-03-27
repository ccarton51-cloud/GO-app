import streamlit as st
import pandas as pd
import re

# 1. Configuration
st.set_page_config(page_title="Coach Grand Oral", page_icon="🎓", layout="wide")

def get_drive_direct_link(url):
    if pd.isna(url) or "drive.google.com" not in str(url): return url
    file_id = re.search(r'/d/([a-zA-Z0-9-_]+)', str(url))
    return f"https://drive.google.com/uc?export=view&id={file_id.group(1)}" if file_id else url

# Identifiant de ton Sheet
SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet="

st.title("🎓 Coach Grand Oral")

# 2. Navigation
menu = st.sidebar.radio("Navigation", 
    ["Home", "Compétences fondamentales", "ZEN", "Exercices ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

try:
    onglet_nom = menu.replace(" ", "%20")
    df = pd.read_csv(BASE_URL + onglet_nom)
    df = df.fillna("")

    # Nettoyage des noms de colonnes
    df.columns = [c.strip().lower() for c in df.columns]

    if menu == "Home":
        for i, row in df.iterrows():
            titre = row.get('nom', '')
            if titre: st.header(titre)
            
            # Affichage de l'image principale si elle existe dans le sheet
            if 'image' in df.columns and row['image'] != "":
                st.image(get_drive_direct_link(row['image']), use_container_width=True)
            
            # Affichage des textes (texte, texte 1, texte 2...)
            for c in df.columns:
                if 'texte' in c and row[c] != "": st.write(row[c])
            
            # --- AJOUT SPÉCIFIQUE POUR "L'ÉPREUVE" ---
            if "épreuve" in titre.lower():
                st.write("---")
                col1, col2 = st.columns(2)
                with col1:
                    st.image(get_drive_direct_link("https://drive.google.com/file/d/12vSOPi3k8Nca-iJOFxaM0mHQT9tK6rBp/view?usp=sharing"), caption="Focus Épreuve 1")
                with col2:
                    st.image(get_drive_direct_link("https://drive.google.com/file/d/1YgJDvx7XRn4ltvS6yGDPe3IOVum0VNSj/view?usp=sharing"), caption="Focus Épreuve 2")
                st.write("---")

    elif menu == "Compétences fondamentales":
        st.header("Les Fondamentaux")
        for i, row in df.iterrows():
            with st.container(border=True):
                if 'image' in df.columns and row['image'] != "": 
                    st.image(get_drive_direct_link(row['image']), width=400)
                if 'texte' in df.columns: st.info(row['texte'])

    elif menu == "ZEN":
        st.header("Plan ZEN")
        for i, row in df.iterrows():
            titre_zen = row.get('nom', f"Exercice {i+1}")
            with st.expander(f"🧘 {titre_zen}", expanded=True):
                c1, c2 = st.columns([1, 2])
                with c1:
                    if 'logo' in df.columns and row['logo'] != "":
                        st.image(get_drive_direct_link(row['logo']), width=150)
                with c2:
                    if 'texte' in df.columns: st.write(row['texte'])
                if 'image' in df.columns and row['image'] != "":
                    st.image(get_drive_direct_link(row['image']), use_container_width=True)

    elif "Exercices" in menu:
        st.header(menu)
        for i, row in df.iterrows():
            titre_ex = row.get('nom', 'Détails')
            with st.expander(f"🎯 {titre_ex}"):
                if 'descriptif' in df.columns: st.write(f"**Objectif :** {row['descriptif']}")
                st.divider()
                col_ex = [c for c in df.columns if 'exercice' in c]
                if col_ex: st.write(row[col_ex[0]])
                if 'video' in df.columns and row['video'] != "":
                    st.video(row['video'])
                if 'image' in df.columns and row['image'] != "":
                    st.image(get_drive_direct_link(row['image']))

    elif menu == "Countdown":
        st.header("⏳ Dernières étapes")
        for i, row in df.iterrows():
            st.subheader(f"🗓️ {row.get('nom', '')}")
            cols = st.columns(2)
            with cols[0]:
                for c in df.columns:
                    if 'texte' in c and row[c] != "": st.write(f"✅ {row[c]}")
            with cols[1]:
                if 'conseil' in df.columns and row['conseil'] != "":
                    st.success(f"💡 Conseil : {row['conseil']}")
                if 'détente' in df.columns and row['détente'] != "":
                    st.info(f"🧘 Détente : {row['détente']}")
                if 'affaires' in df.columns and row['affaires'] != "":
                    st.warning(f"🎒 Affaires : {row['affaires']}")
            st.divider()

except Exception as e:
    st.error(f"Erreur technique : {e}")

st.sidebar.markdown("---")
st.sidebar.caption("Coach Grand Oral v1.2")

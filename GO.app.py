import streamlit as st
import pandas as pd
import re

# 1. Configuration
st.set_page_config(page_title="Coach Grand Oral", page_icon="🎓", layout="wide")

def get_drive_direct_link(url):
    if pd.isna(url) or "drive.google.com" not in str(url): return url
    file_id = re.search(r'/d/([a-zA-Z0-9-_]+)', str(url))
    if file_id:
        return f"https://drive.google.com/uc?export=view&id={file_id.group(1)}"
    return url

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
    df.columns = [c.strip().lower() for c in df.columns]

    if menu == "Home":
        for i, row in df.iterrows():
            titre = row.get('nom', '')
            if titre: st.header(titre)
            
            # Affichage des textes
            for c in df.columns:
                if 'texte' in c and row[c] != "": st.write(row[c])
            
            # --- GESTION DES IMAGES AVEC BOUTON DE SECOURS ---
            if 'image' in df.columns and row['image'] != "":
                img_url = get_drive_direct_link(row['image'])
                try:
                    st.image(img_url, use_container_width=True)
                except:
                    st.warning("L'image met du temps à charger...")
                st.link_button("🖼️ Voir l'image en grand", row['image'])

            # --- LES 2 IMAGES SPÉCIFIQUES QUE TU VOULAIS ---
            if "épreuve" in str(titre).lower():
                st.divider()
                st.write("### Documents clés pour l'épreuve :")
                c1, c2 = st.columns(2)
                links = [
                    "https://drive.google.com/file/d/12vSOPi3k8Nca-iJOFxaM0mHQT9tK6rBp/view?usp=sharing",
                    "https://drive.google.com/file/d/1YgJDvx7XRn4ltvS6yGDPe3IOVum0VNSj/view?usp=sharing"
                ]
                with c1:
                    st.image(get_drive_direct_link(links[0]), caption="Focus 1")
                    st.link_button("Ouvrir Focus 1", links[0])
                with c2:
                    st.image(get_drive_direct_link(links[1]), caption="Focus 2")
                    st.link_button("Ouvrir Focus 2", links[1])

    # Le reste des onglets suit la même logique simplifiée
    elif menu == "Compétences fondamentales":
        for i, row in df.iterrows():
            with st.container(border=True):
                if 'texte' in df.columns: st.info(row['texte'])
                if 'image' in df.columns and row['image'] != "":
                    st.image(get_drive_direct_link(row['image']), width=300)
                    st.link_button("Voir schéma", row['image'])

    elif menu == "ZEN":
        for i, row in df.iterrows():
            with st.expander(f"🧘 {row.get('nom', 'Exercice')}"):
                if 'texte' in df.columns: st.write(row['texte'])
                if 'image' in df.columns and row['image'] != "":
                    st.image(get_drive_direct_link(row['image']))

    elif "Exercices" in menu:
        for i, row in df.iterrows():
            with st.expander(f"🎯 {row.get('nom', 'Détails')}"):
                if 'exercice' in df.columns: st.write(row['exercice'])
                if 'video' in df.columns and row['video'] != "":
                    st.video(row['video'])

    elif menu == "Countdown":
        for i, row in df.iterrows():
            st.subheader(f"🗓️ {row.get('nom', '')}")
            if 'conseil' in df.columns: st.success(row['conseil'])
            for c in df.columns:
                if 'texte' in c and row[c] != "": st.write(f"✅ {row[c]}")
            st.divider()

except Exception as e:
    st.error(f"Erreur : {e}")

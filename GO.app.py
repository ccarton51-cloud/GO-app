import streamlit as st
import pandas as pd
import re

# Configuration
st.set_page_config(page_title="Coach Grand Oral", page_icon="🎓")

# Fonction pour transformer un lien Google Drive en lien image direct
def get_drive_direct_link(url):
    if "drive.google.com" in str(url):
        file_id = re.search(r'/d/([a-zA-Z0-9-_]+)', str(url))
        if file_id:
            return f"https://drive.google.com/uc?export=view&id={file_id.group(1)}"
    return url

# Chargement des données
DATA_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRzSDyuo96xrlEUrFzj4J4JYrms_qXtcDVOwfm6gI19vWm_Cl10EN4DAUGPXnmNQkASfKURL9b_TC0n/pub?output=csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_URL)

try:
    df = load_data()
    
    st.title("🚀 Objectif Grand Oral")
    
    tabs = st.tabs(["📋 L'Épreuve", "💡 Fondamentaux", "🧘 Plan ZEN", "⏳ J-7 à J"])

    # --- ONGLET 1 : L'ÉPREUVE (Détaillé avec tes colonnes) ---
    with tabs[0]:
        st.header("Tout savoir sur l'épreuve")
        
        # On cherche la ligne où la colonne 'Nom' contient 'L\'épreuve'
        # Note : On adapte selon tes noms de colonnes exacts
        row_epreuve = df[df['Nom'].str.contains("épreuve", case=False, na=False)]
        
        if not row_epreuve.empty:
            data = row_epreuve.iloc[0]
            
            # Affichage de l'image principale si elle existe
            if pd.notna(data.get('Image')):
                st.image(get_drive_direct_link(data['Image']), use_column_width=True)
            
            # Affichage des textes
            for col in ['texte', 'texte 1', 'texte 2', 'texte 3', 'texte 4']:
                if pd.notna(data.get(col)):
                    st.write(data[col])
            
            # Affichage des images secondaires
            cols_img = st.columns(3)
            for i, col_name in enumerate(['image 1', 'image 2', 'image 3']):
                if pd.notna(data.get(col_name)):
                    with cols_img[i]:
                        st.image(get_drive_direct_link(data[col_name]))
            
            # Affichage de la vidéo (si c'est un lien YouTube)
            if pd.notna(data.get('video')):
                if "youtube.com" in str(data['video']) or "youtu.be" in str(data['video']):
                    st.video(data['video'])
                else:
                    st.link_button("🎥 Voir la vidéo", data['video'])

    # --- LES AUTRES ONGLETS (Reste inchangé pour l'instant) ---
    with tabs[1]:
        st.write("Contenu des compétences...")
    with tabs[2]:
        st.write("Contenu Plan ZEN...")
    with tabs[3]:
        st.write("Contenu J-7...")

except Exception as e:
    st.error(f"Erreur de lecture : {e}")

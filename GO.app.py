import streamlit as st
import pandas as pd
import re

# 1. Configuration de la page
st.set_page_config(page_title="Coach Grand Oral", page_icon="🎓", layout="wide")

# --- 2. LA FONCTION MAGIQUE DE CONVERSION DES LIENS DRIVE ---
def get_drive_direct_link(url):
    """
    Transforme un lien Google Drive standard (view) en lien de téléchargement direct pour affichage.
    """
    if pd.isna(url) or "drive.google.com" not in str(url):
        # Si ce n'est pas un lien Drive ou si c'est vide, on ne fait rien
        return url
    
    # On cherche l'ID unique du fichier dans le lien avec une expression régulière
    file_id_match = re.search(r'/d/([a-zA-Z0-9-_]+)', str(url))
    
    if file_id_match:
        file_id = file_id_match.group(1)
        # On reconstruit le lien de téléchargement direct
        direct_link = f"https://drive.google.com/uc?export=view&id={file_id}"
        return direct_link
    
    # Si on ne trouve pas l'ID, on renvoie le lien original par sécurité
    return url

# --- 3. CONFIGURATION DE LA SOURCE DE DONNÉES ---
# Ton identifiant Google Sheet unique
SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"
# URL de base pour l'export CSV
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet="

# --- 4. TITRE DE L'APPLICATION ---
st.title("🎓 Coach Grand Oral")

# --- 5. NAVIGATION (Menu latéral) ---
# J'ai repris l'ordre exact de tes onglets d'après tes images
menu = st.sidebar.radio("Navigation", 
    ["Home", "Compétences fondamentales", "ZEN", "Exercices ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

# --- 6. CHARGEMENT ET AFFICHAGE DES DONNÉES ---
try:
    # On prépare l'URL de l'onglet sélectionné (on encode les espaces avec %20)
    onglet_nom_encode = menu.replace(" ", "%20")
    url_complete = BASE_URL + onglet_nom_encode
    
    # Lecture des données
    df = pd.read_csv(url_complete)
    # Nettoyage : on remplace les cases vides (NaN) par du texte vide pour éviter les erreurs
    df = df.fillna("") 
    
    # Nettoyage des noms de colonnes : tout en minuscules et sans espaces
    # Cela permet de trouver 'nom' même si dans le sheet c'est écrit 'Nom '
    df.columns = [c.strip().lower() for c in df.columns]

    if menu == "Home":
        st.header("Bienvenue sur ton Coach Grand Oral")
        for i, row in df.iterrows():
            if 'nom' in df.columns and row['nom'] != "":
                st.subheader(row['nom'])
            
            # --- ICI, ON UTILISE LA FONCTION DE CONVERSION POUR L'IMAGE PRINCIPALE ---
            if 'image' in df.columns and row['image'] != "":
                st.image(get_drive_direct_link(row['image']), use_container_width=True)
                
            # Affichage des colonnes de texte (texte, texte 1, texte 2...)
            for col in df.columns:
                if 'texte' in col and row[col] != "":
                    st.write(row[col])
            st.divider()

    elif menu == "Compétences fondamentales":
        st.header("Les Compétences à Maîtriser")
        for i, row in df.iterrows():
            with st.container(border=True):
                if 'image' in df.columns and row['image'] != "":
                    # --- CONVERSION ICI AUSSI ---
                    st.image(get_drive_direct_link(row['image']), width=400)
                if 'texte' in df.columns and row['texte'] != "":
                    st.info(row['texte'])

    elif menu == "ZEN":
        st.header("Ton Plan ZEN")
        for i, row in df.iterrows():
            exercice_titre = row.get('nom', f"Exercice {i+1}")
            with st.expander(f"🧘 {exercice_titre}", expanded=True):
                c1, c2 = st.columns([1, 2])
                with c1:
                    # --- CONVERSION ICI POUR LE LOGO ---
                    if 'logo' in df.columns and row['logo'] != "":
                        st.image(get_drive_direct_link(row['logo']), width=150)
                with c2:
                    if 'texte' in df.columns and row['texte'] != "":
                        st.write(row['texte'])
                # --- CONVERSION ICI POUR L'IMAGE DE L'EXERCICE ---
                if 'image' in df.columns and row['image'] != "":
                    st.image(get_drive_direct_link(row['image']), use_container_width=True)

    elif "Exercices" in menu:
        st.header(menu)
        for i, row in df.iterrows():
            ex_titre = row.get('nom', 'Détails')
            with st.expander(f"🎯 {ex_titre}"):
                if 'descriptif' in df.columns and row['descriptif'] != "":
                    st.write(f"**Objectif :** {row['descriptif']}")
                st.divider()
                
                # On cherche la colonne qui contient le mot 'exercice'
                col_exercice = [c for c in df.columns if 'exercice' in c]
                if col_exercice and row[col_exercice[0]] != "":
                    st.write(row[col_exercice[0]])
                
                if 'video' in df.columns and row['video'] != "":
                    st.video(row['video'])
                    
                # --- CONVERSION ICI POUR L'IMAGE DE L'EXERCICE ---
                if 'image' in df.columns and row['image'] != "":
                    st.image(get_drive_direct_link(row['image']))

    elif menu == "Countdown":
        st.header("⏳ La Dernière Ligne Droite")
        for i, row in df.iterrows():
            st.subheader(f"🗓️ {row.get('nom', '')}")
            cols = st.columns(2)
            with cols[0]:
                st.write("**À Faire :**")
                # On affiche toutes les colonnes qui contiennent 'texte'
                for col in df.columns:
                    if 'texte' in col and row[col] != "":
                        st.write(f"- {row[col]}")
            with cols[1]:
                if 'conseil' in df.columns and row['conseil'] != "":
                    st.success(f"💡 Conseil : {row['conseil']}")
                if 'détente' in df.columns and row['détente'] != "":
                    st.info(f"🧘 Détente : {row['détente']}")
                if 'affaires' in df.columns and row['affaires'] != "":
                    st.warning(f"🎒 Affaires : {row['affaires']}")
            st.divider()

except Exception as e:
    st.error(f"Erreur lors du chargement de l'onglet '{menu}'.")
    st.write("Détails de l'erreur :", e)
    st.info("Vérifie que ton Google Sheet est bien partagé en mode 'Tous les utilisateurs avec le lien'.")

st.sidebar.markdown("---")
st.sidebar.caption("Coach Grand Oral v1.1 | Fait avec ❤️ pour tes élèves.")

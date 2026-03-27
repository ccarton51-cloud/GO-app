import streamlit as st
import pandas as pd
import re

# --- PARTIE MODIFIÉE POUR L'ICÔNE (FAVICON) ---
# Lien direct vers ton logo "points" sur GitHub
LOGO_URL = "https://raw.githubusercontent.com/ccarton51-cloud/GO-app/main/images/logo.png"

# Configuration de la page avec ton logo personnalisé
st.set_page_config(
    page_title="Coach Grand Oral",
    page_icon=LOGO_URL, # <--- C'est ici que le changement opère !
    layout="wide"
)
def get_link(url):
    # Sécurité absolue : si c'est pas du texte ou si c'est trop court, on ignore
    if pd.isna(url) or len(str(url)) < 10: 
        return None
    
    url = str(url).strip()
    
    # SI LE LIEN NE COMMENCE PAS PAR HTTP, ON L'IGNORE (bye bye les "0")
    if not url.lower().startswith('http'):
        return None

    # Conversion GitHub Raw
    if "github.com" in url and "raw" not in url:
        url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    
    return url

# 2. Paramètres Google Sheet
SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet="

# 3. Titre principal et Sidebar (Ajustement du menu pour inclure "L'épreuve")
st.sidebar.title("Navigation")
menu = st.sidebar.radio("", 
    ["Home", "L'épreuve", "Compétences fondamentales", "ZEN", "Exercices ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

# --- PAGE ACCUEIL (HOME) ---
if menu == "Home":
    st.title("🎓 Coach Grand Oral")
    
    # --- PARTIE MODIFIÉE POUR LE LOGO ---
    # Nous utilisons le lien direct (Raw) vers ton image sur GitHub
    logo_url = "https://raw.githubusercontent.com/ccarton51-cloud/GO-app/main/images/logo.png"
    
    # Affichage du logo. Tu peux ajuster 'width' pour changer la taille.
    st.image(logo_url, width=200)
    # -------------------------------------

    # Ton texte de bienvenue
    st.markdown("""
    Bienvenue dans ton allié ultime pour réussir le Grand Oral.  
    Cette application a été conçue comme un véritable aide-mémoire, simple et efficace, pour t’accompagner partout dans ta préparation. Tu y trouveras tout l’essentiel pour aborder l’épreuve avec confiance : le déroulement détaillé du Grand Oral pour savoir exactement à quoi t’attendre, des “plans zen” pour apprendre à gérer ton stress et rester seren, ainsi que des exercices pratiques pour maîtriser les fondamentaux de la prise de parole — ethos, pathos, logos — et faire passer ton message avec impact.  
    
    Pour profiter pleinement de toutes ces ressources, utilise la navigation de l’application afin d’accéder facilement aux différentes sections et avancer à ton rythme.  
    
    Parce que la réussite se construit aussi dans les derniers jours, un compte à rebours t’accompagne de J-7 jusqu’au jour J, avec des rappels et des conseils pour rester concentré et prêt au bon moment.  
    
    Que tu sois en train de commencer tes révisions ou dans la dernière ligne droite, cette application est là pour te guider, t’entraîner et te rassurer. À toi de jouer.
    """)

# --- AUTRES PAGES (DYNAMIQUES via Google Sheet) ---
else:
    try:
        # Encodage spécial pour gérer l'apostrophe dans "L'épreuve"
        onglet_nom = menu.replace(" ", "%20").replace("'", "%27")
        df = pd.read_csv(BASE_URL + onglet_nom).fillna("")
        
        # Nettoyage des noms de colonnes
        df.columns = [c.strip().lower() for c in df.columns]

        for i, row in df.iterrows():
            # Titre section
            nom = str(row.get('nom', '')).strip()
            if nom and nom not in ["0", "nan"]:
                st.header(nom)
            
            # Texte principal
            txt = str(row.get('texte', '')).strip()
            if txt and txt not in ["0", "nan"]:
                st.write(txt)

            # GESTION DES IMAGES (Colonnes image 1, image 2, etc.)
            cols_img = [c for c in df.columns if 'image' in c]
            liens_valides = []
            
            for c in cols_img:
                link = get_link(row[c])
                if link:
                    liens_valides.append(link)
            
            # Affichage des images trouvées
            if liens_valides:
                if len(liens_valides) > 1:
                    cols = st.columns(len(liens_valides))
                    for idx, l in enumerate(liens_valides):
                        cols[idx].image(l, use_container_width=True)
                else:
                    st.image(liens_valides[0], use_container_width=True)

            # Vidéo
            if 'video' in df.columns:
                v = str(row['video']).strip()
                if v.startswith('http'):
                    st.video(v)
                
            # Textes secondaires
            for c in df.columns:
                if 'texte' in c and c != 'texte':
                    val = str(row[c]).strip()
                    if val and val not in ["0", "nan"]:
                        st.write(val)
            
            st.divider()

    except Exception as e:
        # Message d'information si l'onglet n'existe pas encore dans le Sheet
        st.info("Sélectionnez une section dans le menu pour afficher le contenu.")

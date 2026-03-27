import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Diagnostic Coach", layout="wide")

# 1. Paramètres
SHEET_ID = "1cAvqijg9fPLCLNEg9ip0nw2KSJLH9a7SvJqe31IYbHU"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet="

# 2. Menu
menu = st.sidebar.radio("Navigation", ["Home", "L'épreuve", "Compétences fondamentales", "ZEN", "L'ETHOS", "Exercices LOGOS", "Exercices PATHOS", "Countdown"])

st.write(f"### Diagnostic : Onglet sélectionné = **{menu}**")

try:
    # On force la lecture du Sheet sans aucun cache
    url = f"{BASE_URL}{urllib.parse.quote(menu)}&cachebust={pd.Timestamp.now().timestamp()}"
    df = pd.read_csv(url).fillna("")
    
    # Affichage des colonnes détectées pour comprendre le bug
    colonnes_trouvees = list(df.columns)
    st.info(f"Colonnes détectées dans cet onglet : {colonnes_trouvees}")

    if menu == "L'ETHOS":
        # On force l'affichage brut pour voir ce qui arrive du Sheet
        for i, row in df.iterrows():
            nom = str(row.get('Nom', row.get('nom', '')))
            if nom and nom.lower() not in ["nan", "0", ""]:
                st.subheader(f"Nom : {nom}")
                
                # Image
                img_col = 'image' if 'image' in df.columns else 'logo'
                link = str(row.get(img_col, ''))
                if "http" in link:
                    # Conversion lien raw automatique
                    final_link = link.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/").split('?')[0]
                    st.image(final_link, width=400)
                
                # Descriptif
                st.write(f"**Descriptif :** {row.get('descriptif', row.get('Descriptif', 'N/A'))}")
                
                # Exercice
                st.info(f"**Exercice :** {row.get('exercice', row.get('Exercice', 'N/A'))}")
                st.divider()
    else:
        st.write("Contenu des autres pages (en attente de validation Ethos)")
        st.dataframe(df.head(3)) # Affiche un aperçu du tableau pour vérifier les données

except Exception as e:
    st.error(f"Erreur technique : {e}")

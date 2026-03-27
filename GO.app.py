import streamlit as st
import pandas as pd

# Configuration de l'interface mobile-friendly
st.set_page_config(page_title="Coach Grand Oral", page_icon="🎓")

# Style CSS personnalisé pour rendre l'app plus "zen"
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; }
    .exercice-card { 
        padding: 20px; 
        border-radius: 10px; 
        background-color: white; 
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# Chargement des données
DATA_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRzSDyuo96xrlEUrFzj4J4JYrms_qXtcDVOwfm6gI19vWm_Cl10EN4DAUGPXnmNQkASfKURL9b_TC0n/pub?output=csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    return df

try:
    df = load_data()
    
    st.title("🚀 Objectif Grand Oral")
    st.write("Ton guide complet pour réussir l'épreuve avec sérénité.")

    # Système de navigation par onglets
    menu = st.tabs(["📋 L'Épreuve", "💡 Fondamentaux", "🧘 Plan ZEN", "⏳ J-7 à J"])

    # --- ONGLET 1 : L'ÉPREUVE ---
    with menu[0]:
        st.header("Tout savoir sur l'épreuve")
        if 'L\'épreuve' in df.columns:
            for item in df['L\'épreuve'].dropna():
                st.info(item)

    # --- ONGLET 2 : COMPÉTENCES ---
    with menu[1]:
        st.header("Compétences Fondamentales")
        if 'Compétences fondalementales' in df.columns:
            for item in df['Compétences fondalementales'].dropna():
                with st.expander("🔍 Voir le conseil"):
                    st.write(item)

    # --- ONGLET 3 : PLAN ZEN ---
    with menu[2]:
        st.header("Ton Plan ZEN")
        st.subheader("Préparation physique et mentale")
        if 'Plan ZEN' in df.columns:
            for exercice in df['Plan ZEN'].dropna():
                st.markdown(f"""<div class="exercice-card">{exercice}</div>""", unsafe_allow_html=True)

    # --- ONGLET 4 : CALENDRIER ---
    with menu[3]:
        st.header("Dernière ligne droite")
        if 'De J-7 à J' in df.columns:
            # On affiche les conseils sous forme de timeline
            for conseil in df['De J-7 à J'].dropna():
                st.warning(conseil)

except Exception as e:
    st.error("Oups ! Connexion au Google Sheet interrompue.")
    st.write("Vérifie que le lien de publication CSV est correct.")

st.sidebar.caption("Fait avec ❤️ pour tes élèves.")
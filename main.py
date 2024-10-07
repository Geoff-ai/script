import streamlit as st
from scripts import maillage_interne





# Configuration des pages
PAGES = {
    "Analyse kefehgie": maillage_interne

}

# Titre principal
st.sidebar.title("KakaSEO")

# Sous-titre et choix des scripts
st.sidebar.subheader("Les scripts")
selection = st.sidebar.radio("", list(PAGES.keys()), index=0)

# Affichage du script sélectionné
page = PAGES[selection]
page.app()

# Copyright
st.sidebar.markdown("©️ 2024 | by KakaSEO")

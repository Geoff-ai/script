import streamlit as st
from scripts import description_produits



# Configuration des pages
PAGES = {
    "Desc produits": description_produits

}

# Titre principal
st.sidebar.title("roykyserpking")

# Sous-titre et choix des scripts
st.sidebar.subheader("Les scripts")
selection = st.sidebar.radio("", list(PAGES.keys()), index=0)

# Affichage du script sélectionné
page = PAGES[selection]
page.app()

# Copyright
st.sidebar.markdown("©️ 2024 | by roykyserpking")

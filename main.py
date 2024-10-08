import streamlit as st
from scripts import description_produits

# Configuration des pages
PAGES = {
    "Analyse description des produits": description_produits.app
}

# Titre principal
st.sidebar.title("roykyserpking")

# Sous-titre et choix des scripts
st.sidebar.subheader("Les scripts")
selection = st.sidebar.radio("", list(PAGES.keys()), index=0)

# Affichage du script sélectionné
page = PAGES[selection]

# Appel de la fonction app() du module sélectionné
page()  # Exécute la fonction app() de description_produits

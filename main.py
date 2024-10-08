import streamlit as st
from scripts import description_produits

# Configuration des pages
PAGES = {
    "Analyse description des produits": description_produits.traiter_fichier_excel
}

# Menu latéral
st.sidebar.title("Menu")
selection = st.sidebar.radio("Choisissez une option", list(PAGES.keys()))

# Appelle la fonction de la page sélectionnée
page = PAGES[selection]
page()

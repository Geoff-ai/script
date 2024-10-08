import streamlit as st
from scripts import description_produits

# Configuration des pages
PAGES = {
    "Analyse description des produits": description_produits.traiter_fichier_excel
}

# Titre principal
st.sidebar.title("Interface de description de produits")

# Sous-titre et choix des scripts
st.sidebar.subheader("Les scripts disponibles")
selection = st.sidebar.radio('', list(PAGES.keys()), index=0)

# Affichage du script sélectionné
page = PAGES[selection]

# Appel de la fonction app() du module sélectionné
fichier = st.file_uploader("Choisissez un fichier Excel", type="xlsx")

if fichier:
    page(fichier)

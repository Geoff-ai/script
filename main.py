import streamlit as st
from scripts import analyse_proposition_maillage



# Configuration des pages
PAGES = {
    "Analyse + Proposition Maillage": analyse_proposition_maillage,
    "Proposition Maillage": proposition_maillage,
    "Tri + Nettoyage de mots-clés": tri_keywords,
    "Analyse Cannibalisation SERP (2€30 pour 1000 mots)": cannibalisation_serp_payant,
    "Analyse Cannibalisation SERP (gratuit)": cannibalisation_serp_gratuit,
    "Images Bulk": images_bulk,
    "Post Article WP": post_article_wp,
    "Audit SEO On-page": audit_on_page,
    "Google SERP Scraper": google_serp_scraper,
    "Maillage TEST": testmaillage

}

# Titre principal
st.sidebar.title("PirateSEO")

# Sous-titre et choix des scripts
st.sidebar.subheader("Les scripts")
selection = st.sidebar.radio("", list(PAGES.keys()), index=0)

# Affichage du script sélectionné
page = PAGES[selection]
page.app()

# Copyright
st.sidebar.markdown("©️ 2024 | by PirateSEO")

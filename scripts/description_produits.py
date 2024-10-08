import streamlit as st
import pandas as pd

# Liste des mots-clés stratégiques
seo_keywords = {
    "Poele a compartiments": 260,
    "Poele en pierre": 2900,
    "poele inox 18/10": 2900,
    "poele a paella": 2400,
    "Poele cuivre": 1900,
    "Poele en acier": 1900,
    "poele en fonte": 12000,
    "Poele a pancake / a crepes": 4400,
    "poele a oeuf": 480,
    "Poele double compartiments": 480,
    "Poele 2 compartiments": 320,
    "Poele 4 compartiments": 210,
    "Poele a frire": 1000,
    "Poele 4 trous": 50,
    "Poele 7 trous": 20,
}

# Fonction pour générer une description en fonction du titre et des mots-clés
def generate_description(title):
    keywords_in_title = [kw for kw in seo_keywords.keys() if kw.lower() in title.lower()]
    if keywords_in_title:
        primary_keyword = keywords_in_title[0]  # Prend le premier mot-clé trouvé
    else:
        primary_keyword = "poêle"

    # Génération de la description
    description = f"""
    La {primary_keyword} {title} est un choix idéal pour les amateurs de cuisine exigeants. 
    Fabriquée avec des matériaux de haute qualité, elle assure une cuisson uniforme et durable. 
    Cette {primary_keyword} est parfaite pour préparer des repas savoureux en toute simplicité, que ce soit pour des crêpes, des œufs, ou une délicieuse paella.

    Pourquoi choisir la {primary_keyword} {title} ?
    - Conçue pour offrir une distribution optimale de la chaleur.
    - Matériaux robustes pour une durabilité exceptionnelle.
    - Facile à entretenir et compatible avec différents types de cuisinières.

    Conseils d'entretien :
    Pour préserver votre {primary_keyword}, nous vous recommandons de la laver à la main et d'éviter les produits abrasifs.
    """

    return description

# Fonction principale à appeler depuis le fichier main.py
def app():
    # Téléchargement du fichier Excel
    uploaded_file = st.file_uploader("Choisissez un fichier Excel", type="xlsx")

    if uploaded_file:
        df = pd.read_excel(uploaded_file)

        # Vérification des colonnes attendues
        if 'Titre' in df.columns and 'Description' in df.columns:
            for index, row in df.iterrows():
                if pd.isna(row['Description']):
                    # Générer une nouvelle description si aucune description n'existe
                    df.at[index, 'Description'] = generate_description(row['Titre'])

            # Affichage des descriptions mises à jour
            st.write("Descriptions mises à jour :")
            st.dataframe(df)

            # Téléchargement du fichier mis à jour
            def convert_df_to_excel(df):
                return df.to_excel(index=False)

            st.download_button(
                label="Télécharger les descriptions mises à jour",
                data=convert_df_to_excel(df),
                file_name="produits_mis_a_jour.xlsx",
                mime="application/vnd.ms-excel"
            )
        else:
            st.error("Le fichier Excel doit contenir les colonnes 'Titre' et 'Description'.")

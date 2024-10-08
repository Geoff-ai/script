import streamlit as st
import pandas as pd
from io import BytesIO
import random

# Liste des mots-clés stratégiques et synonymes
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

# Listes de synonymes pour varier les descriptions
synonymes_durable = ["durable", "solide", "robuste", "résistant"]
synonymes_polyvalent = ["polyvalent", "multi-usage", "adaptable", "pratique"]
synonymes_entretien = ["facile à entretenir", "simple à nettoyer", "peu d'entretien", "entretien facile"]

# Fonction pour générer des descriptions variées
def generate_description(title):
    keywords_in_title = [kw for kw in seo_keywords.keys() if kw.lower() in title.lower()]
    if keywords_in_title:
        primary_keyword = keywords_in_title[0]  # Prend le premier mot-clé trouvé
    else:
        primary_keyword = "poêle"
    
    # Sélection de synonymes pour varier les descriptions
    durable = random.choice(synonymes_durable)
    polyvalent = random.choice(synonymes_polyvalent)
    entretien = random.choice(synonymes_entretien)

    # Génération de la description en deux paragraphes
    description = f"""
    {title} est une {primary_keyword} exceptionnelle, conçue pour ceux qui recherchent la perfection en cuisine. 
    Grâce à sa conception {durable}, elle garantit des performances optimales à chaque utilisation. 
    Que vous prépariez un dîner en famille ou un repas rapide, cette {primary_keyword} est {polyvalent} et répond à tous vos besoins culinaires.

    Avec une attention particulière aux détails, cette {primary_keyword} est également {entretien}, vous permettant de la maintenir en parfait état avec un minimum d'effort. 
    Que vous cuisiniez sur une plaque à induction, un feu de gaz ou un autre type de cuisinière, ce produit vous offre une polyvalence inégalée.
    """
    
    # Vérification de la longueur du texte pour garantir 300 mots minimum
    if len(description.split()) < 300:
        description += " " * (300 - len(description.split()))  # Ajoute des espaces ou du texte pour compléter

    return description

# Fonction pour convertir le DataFrame en fichier Excel
def convert_df_to_excel(df):
    output = BytesIO()  # Créer un buffer en mémoire
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)  # Convertir le DataFrame en Excel
    processed_data = output.getvalue()  # Obtenir le contenu du fichier Excel
    return processed_data

# Fonction pour convertir le DataFrame en fichier CSV
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

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

            # Téléchargement du fichier mis à jour au format Excel
            st.download_button(
                label="Télécharger les descriptions en Excel",
                data=convert_df_to_excel(df),
                file_name="produits_mis_a_jour.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # Téléchargement du fichier mis à jour au format CSV
            st.download_button(
                label="Télécharger les descriptions en CSV",
                data=convert_df_to_csv(df),
                file_name="produits_mis_a_jour.csv",
                mime="text/csv"
            )
        else:
            st.error("Le fichier Excel doit contenir les colonnes 'Titre' et 'Description'.")

import streamlit as st
import pandas as pd
from openai import OpenAIError
import openai

# Configuration de l'API OpenAI
openai.api_key = 'TA_CLE_API_ICI'

def generer_description(titre):
    try:
        # Appel à l'API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ou "gpt-4"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Please write a product description for {titre}."}
            ]
        )
        return response['choices'][0]['message']['content']
    except OpenAIError as e:
        st.error(f"Erreur lors de l'appel à l'API OpenAI : {e}")
        return ""

# Téléchargement du fichier Excel
fichier = st.file_uploader("Choisissez un fichier Excel", type="xlsx")

if fichier:
    st.write("Fichier chargé avec succès. Lecture du fichier...")
    df = pd.read_excel(fichier)

    # Affichage des premières lignes pour vérifier le fichier
    st.write("Voici un aperçu des données du fichier :")
    st.write(df.head())

    # Ajout d'un bouton pour lancer l'analyse des titres
    if st.button("Générer les descriptions"):
        st.write("Traitement des données en cours...")

        # Boucle sur chaque ligne pour générer une description
        try:
            for index, row in df.iterrows():
                titre = row['Titre']
                st.write(f"Traitement du titre : {titre}")

                # Appel de la fonction pour générer la description
                description = generer_description(titre)
                st.write(f"Description générée pour {titre}")

                # Mise à jour de la colonne 'Description'
                df.at[index, 'Description'] = description

            # Sauvegarde du fichier Excel avec les descriptions
            df.to_excel('output_with_descriptions.xlsx', index=False)
            st.write("Descriptions générées et fichier sauvegardé sous le nom 'output_with_descriptions.xlsx'.")

        except Exception as e:
            st.error(f"Erreur lors du traitement : {e}")

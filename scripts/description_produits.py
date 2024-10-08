import pandas as pd
import openai
import streamlit as st

# Fonction pour traiter le fichier Excel
def traiter_fichier_excel():
    fichier = st.file_uploader("Choisissez un fichier Excel", type="xlsx")

    if fichier is not None:
        df = pd.read_excel(fichier)
        st.write("Fichier chargé avec succès. Voici un aperçu des données :")
        st.write(df.head())

        # Boucle sur chaque ligne du fichier Excel
        for index, row in df.iterrows():
            titre = row['Titre']  # Assurez-vous que la colonne s'appelle 'Titre'
            description = generer_description(titre)
            df.at[index, 'Description'] = description

        # Sauvegarde du fichier avec les descriptions
        df.to_excel('output_with_descriptions.xlsx', index=False)
        st.write("Fichier généré avec succès et téléchargé.")

# Fonction pour générer une description en utilisant l'API OpenAI
def generer_description(titre):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Please write a product description for {titre}."}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"Erreur avec l'API OpenAI : {e}")
        return ""

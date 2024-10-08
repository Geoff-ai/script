import pandas as pd
import openai
import streamlit as st
import io

# Fonction pour traiter le fichier Excel
def traiter_fichier_excel():
    fichier = st.file_uploader("Choisissez un fichier Excel", type="xlsx")

    if fichier is not None:
        try:
            df = pd.read_excel(fichier)
            if 'Titre' not in df.columns:
                st.error("Le fichier Excel doit contenir une colonne 'Titre'.")
                return
            
            if 'Description' not in df.columns:
                df['Description'] = ""  # Ajoute la colonne 'Description' si elle n'existe pas

            st.write("Fichier chargé avec succès. Voici un aperçu des données :")
            st.write(df.head())

            # Boucle sur chaque ligne du fichier Excel
            for index, row in df.iterrows():
                titre = row['Titre']  # Assurez-vous que la colonne s'appelle 'Titre'
                description = generer_description(titre)
                df.at[index, 'Description'] = description

            # Sauvegarde du fichier avec les descriptions dans un buffer mémoire
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)

            st.write("Descriptions générées avec succès !")

            # Ajout d'un bouton de téléchargement pour le fichier Excel généré
            st.download_button(
                label="Télécharger le fichier avec descriptions",
                data=buffer,
                file_name="output_with_descriptions.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier Excel : {e}")

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

# Appel de la fonction principale
if __name__ == "__main__":
    st.title("Générateur de descriptions de produits")
    traiter_fichier_excel()

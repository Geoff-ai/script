import streamlit as st
import pandas as pd
import openai

# Fonction pour générer des descriptions
def generate_descriptions(api_key, selected_column, df):
    openai.api_key = api_key
    descriptions = []
    
    for title in df[selected_column]:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": ""},
                    {"role": "user", "content": title}  # Remplis avec le prompt souhaité
                ],
                temperature=1
            )
            descriptions.append(response['choices'][0]['message']['content'].strip())  # Utiliser .strip() pour éviter les espaces inutiles
        except Exception as e:
            st.error(f"Erreur lors de la génération pour '{title}': {str(e)}")
            descriptions.append("")  # Ajouter une description vide en cas d'erreur
    
    df['Description'] = descriptions
    return df

def app():
    st.title("Générateur de descriptions de produits")

    # Chargement du fichier
    uploaded_file = st.file_uploader("Téléchargez un fichier .xlsx ou .csv", type=['xlsx', 'csv'])
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        # Affichage des colonnes du DataFrame
        st.write("Colonnes disponibles :", df.columns.tolist())
        
        # Sélection de la colonne des titres
        selected_column = st.selectbox("Sélectionnez la colonne des titres", df.columns.tolist())

        # Champ pour la clé API
        api_key = st.text_input("Entrez votre clé API OpenAI", type="password")

        if st.button("Générer les descriptions"):
            if api_key and selected_column:
                with st.spinner("Génération en cours..."):
                    updated_df = generate_descriptions(api_key, selected_column, df)
                
                st.success("Descriptions générées avec succès !")
                st.write(updated_df)

                # Option pour télécharger le fichier mis à jour
                csv = updated_df.to_csv(index=False)
                st.download_button("Télécharger le fichier mis à jour", csv, "updated_descriptions.csv", "text/csv")
            else:
                st.error("Veuillez entrer la clé API et sélectionner une colonne.")


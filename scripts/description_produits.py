import openai
import pandas as pd
import streamlit as st

# Récupération de la clé API OpenAI à partir de secrets.toml
openai.api_key = st.secrets["openai"]["api_key"]

# Fonction pour générer une description via l'API OpenAI avec le modèle gpt-4o-mini
def generate_description(title, system_prompt, user_prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Utilisation du modèle gpt-4o-mini
            messages=[
                {
                    "role": "system",
                    "content": system_prompt  # Instructions générales sur le comportement du modèle
                },
                {
                    "role": "user",
                    "content": user_prompt.format(title=title)  # Instruction spécifique pour chaque titre
                }
            ],
            temperature=1
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.InvalidRequestError as e:
        st.error(f"Erreur dans la requête OpenAI : {e}")
        return ""

# Définition de l'application Streamlit pour la génération des descriptions
def app():
    st.title("Générateur de descriptions produits")

    # Upload du fichier
    uploaded_file = st.file_uploader("Chargez un fichier .xlsx ou .csv", type=["xlsx", "csv"])

    if uploaded_file is not None:
        # Lecture du fichier dans un dataframe
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        # Sélection de la colonne contenant les titres
        columns = df.columns.tolist()
        title_column = st.selectbox("Sélectionnez la colonne des titres", columns)

        # Affichage du dataframe avant la génération
        st.write("Dataframe initial :")
        st.write(df)

        # Saisie des prompts pour OpenAI
        system_prompt = st.text_area("System prompt", value="You are a helpful assistant that generates product descriptions.")
        user_prompt = st.text_area("User prompt", value="Rédige une description produit de 300 mots pour le titre suivant : {title}")

        # Bouton pour générer les descriptions
        if st.button("Générer les descriptions"):
            # Mise à jour du dataframe avec les descriptions générées
            df['Description'] = df[title_column].apply(lambda x: generate_description(x, system_prompt, user_prompt))

            # Affichage du dataframe mis à jour
            st.write("Dataframe mis à jour :")
            st.write(df)

            # Option pour télécharger le dataframe modifié
            def convert_df(df):
                return df.to_csv(index=False).encode('utf-8')

            csv = convert_df(df)
            st.download_button(label="Télécharger le fichier mis à jour", data=csv, file_name='fichier_mis_a_jour.csv', mime='text/csv')

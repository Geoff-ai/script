import streamlit as st
import pandas as pd
from io import BytesIO
import openpyxl
import openai

# Lire la clé API depuis secrets.toml
openai.api_key = st.secrets["openai"]["api_key"]

# Fonction pour générer des descriptions en utilisant GPT-4o ou GPT-3.5-turbo
def generate_description_gpt(model, title):
    prompt = f"""
    Écris une description unique en 2 paragraphes d'au moins 300 mots pour un produit appelé '{title}'. 
    Intègre les avantages, l'utilisation du produit, ainsi que des conseils d'entretien. 
    Utilise un ton persuasif et assure l'optimisation SEO.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates product descriptions."},
                {"role": "user", "content": prompt}
            ]
        )
        # Utilisation correcte de la réponse avec la nouvelle API
        description = response.choices[0].message["content"].strip()
    except Exception as e:
        st.error(f"Erreur avec l'API OpenAI : {str(e)}")
        description = "Description non générée en raison d'une erreur."

    return description

# Fonction pour convertir le DataFrame en fichier Excel avec openpyxl
def convert_df_to_excel(df):
    output = BytesIO()  # Créer un buffer en mémoire
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)  # Convertir le DataFrame en Excel
    processed_data = output.getvalue()  # Obtenir le contenu du fichier Excel
    return processed_data

# Fonction pour convertir le DataFrame en fichier CSV
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Fonction principale pour exécuter l'application
def app():
    # Téléchargement du fichier Excel
    uploaded_file = st.file_uploader("Choisissez un fichier Excel", type="xlsx")

    if uploaded_file:
        df = pd.read_excel(uploaded_file)

        # Vérification des colonnes attendues
        if 'Titre' in df.columns and 'Description' in df.columns:
            model_choice = st.selectbox(
                "Choisissez le modèle OpenAI à utiliser",
                options=["gpt-3.5-turbo", "gpt-4o"]
            )

            for index, row in df.iterrows():
                if pd.isna(row['Description']) or row['Description'] == "":
                    # Utiliser GPT-4o ou GPT-3.5-turbo pour générer une nouvelle description
                    new_description = generate_description_gpt(model_choice, row['Titre'])
                    df.at[index, 'Description'] = new_description
                else:
                    st.write(f"Description déjà présente pour '{row['Titre']}'")

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

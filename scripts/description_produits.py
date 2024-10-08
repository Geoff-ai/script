import streamlit as st
import pandas as pd
import openai
from io import BytesIO
import openpyxl

# Lire la clé API depuis secrets.toml
openai.api_key = st.secrets["openai"]["api_key"]

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

# Fonction pour générer des descriptions en utilisant l'API OpenAI GPT-4o
def generate_description_gpt4(title):
    prompt = f"""
    Écris une description unique en 2 paragraphes d'au moins 300 mots pour un produit appelé '{title}'. 
    Intègre les avantages, l'utilisation du produit, ainsi que des conseils d'entretien. 
    Utilise un ton persuasif et assure l'optimisation SEO. Voici quelques mots-clés : {', '.join(seo_keywords.keys())}.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates product descriptions."},
                {"role": "user", "content": prompt}
            ]
        )
        description = response['choices'][0]['message']['content'].strip()
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
            for index, row in df.iterrows():
                if pd.isna(row['Description']) or row['Description'] == "":
                    # Utiliser GPT-4o pour générer une nouvelle description
                    new_description = generate_description_gpt4(row['Titre'])
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

import openai
import pandas as pd

# Instancier le client OpenAI avec la clé API
client = openai.OpenAI(api_key="TA_CLE_API")

# Fonction pour générer une description de produit
def generer_description(titre_produit):
    messages = [
        {"role": "system", "content": "Tu es un assistant qui aide à rédiger des descriptions de produits."},
        {"role": "user", "content": f"Rédige une description pour le produit : {titre_produit}. Assure-toi qu'elle fasse au moins 300 mots."}
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # ou gpt-4 selon ton choix
            messages=messages,
            max_tokens=300
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Erreur lors de la génération de la description pour {titre_produit}: {e}")
        return None

# Charger le fichier Excel et générer les descriptions
def traiter_fichier_excel(fichier):
    df = pd.read_excel(fichier)
    
    # Assumer que les titres de produits sont dans la colonne "Titre"
    if 'Titre' not in df.columns:
        print("Le fichier ne contient pas de colonne 'Titre'.")
        return
    
    df['Description'] = df['Titre'].apply(generer_description)
    
    # Sauvegarder les résultats dans un nouveau fichier Excel
    df.to_excel("produits_avec_descriptions.xlsx", index=False)
    print("Descriptions générées et sauvegardées dans 'produits_avec_descriptions.xlsx'.")

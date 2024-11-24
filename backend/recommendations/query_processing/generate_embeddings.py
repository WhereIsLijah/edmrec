# generate_embeddings.py

import os
import sys
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
import joblib
from django.conf import settings
import django

# Ensure the kaggle.json file is in the correct directory
os.environ['KAGGLE_CONFIG_DIR'] = os.path.expanduser('~/.kaggle')

# Add the project root and backend directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'backend'))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from recommendations.models import Metadata, Embedding

# Load or create the TF-IDF vectorizer
tfidf_vectorizer_path = os.path.join(settings.BASE_DIR, 'tfidf_vectorizer.pkl')
tfidf_vectorizer = joblib.load(tfidf_vectorizer_path)
# if os.path.exists(tfidf_vectorizer_path):
#     tfidf_vectorizer = joblib.load(tfidf_vectorizer_path)
#     print("Loaded existing TF-IDF vectorizer.")
# else:
#     tfidf_vectorizer = TfidfVectorizer()
#     print("Created new TF-IDF vectorizer.")

# Load the SentenceTransformer model for BERT embeddings
bert_model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to fetch metadata
def fetch_metadata():
    metadata = Metadata.objects.all().values('id', 'title', 'description')
    df = pd.DataFrame(metadata)
    df['combined_text'] = df['title'].fillna('') + ' ' + df['description'].fillna('')
    return df

# Function to generate TF-IDF embeddings
def generate_tfidf_embeddings(texts):
    if not os.path.exists(tfidf_vectorizer_path):
        # Fit the vectorizer if not already fitted
        tfidf_embeddings = tfidf_vectorizer.fit_transform(texts)
        # Save the vectorizer after fitting
        joblib.dump(tfidf_vectorizer, tfidf_vectorizer_path)
        print("TF-IDF vectorizer fitted and saved.")
    else:
        # Use the loaded vectorizer
        tfidf_embeddings = tfidf_vectorizer.transform(texts)
        print("TF-IDF embeddings generated using existing vectorizer.")
    return tfidf_embeddings

# Function to generate BERT embeddings
def generate_bert_embeddings(texts):
    bert_embeddings = bert_model.encode(texts, show_progress_bar=True)
    return bert_embeddings

# Function to store embeddings
def store_embeddings(df, tfidf_embeddings, bert_embeddings):
    for index, row in df.iterrows():
        tfidf_embedding = tfidf_embeddings[index].toarray().tolist()[0]
        bert_embedding = bert_embeddings[index].tolist()

        embedding, created = Embedding.objects.update_or_create(
            dataset_id=row['id'],
            defaults={
                'tfidf_embedding': tfidf_embedding,
                'bert_embedding': bert_embedding,
                'combined_normalized_text': row['combined_text']
            }
        )
        if created:
            print(f"Created new embedding for dataset ID {row['id']}.")
        else:
            print(f"Updated embedding for dataset ID {row['id']}.")

# Main function
def process_metadata_for_embeddings():
    df = fetch_metadata()

    # Generate embeddings
    tfidf_embeddings = generate_tfidf_embeddings(df['combined_text'])
    bert_embeddings = generate_bert_embeddings(df['combined_text'])

    # Store embeddings
    store_embeddings(df, tfidf_embeddings, bert_embeddings)

# Run the process
if __name__ == "__main__":
    process_metadata_for_embeddings()
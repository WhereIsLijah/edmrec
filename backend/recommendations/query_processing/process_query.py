import os
import logging
import sys
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import joblib
from decouple import config
import django
from django.conf import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root and backend directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'backend'))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from recommendations.models import Metadata, Embedding  # Adjust the import path as needed

# Load the saved TF-IDF vectorizer and BERT model
tfidf_vectorizer_path = os.path.join(settings.BASE_DIR, 'tfidf_vectorizer.pkl')
tfidf_vectorizer = joblib.load(tfidf_vectorizer_path)

bert_model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_tfidf_embedding(query):
    return tfidf_vectorizer.transform([query]).toarray().astype(np.float32)

def generate_bert_embedding(query):
    return bert_model.encode([query])

def process_query(query_text):
    try:
        # Fetch embeddings from the database using Django ORM
        embeddings = Embedding.objects.all().values('dataset_id', 'tfidf_embedding', 'bert_embedding')

        # Create a DataFrame from the queryset
        df = pd.DataFrame(list(embeddings))

        # Convert embeddings from lists to numpy arrays
        tfidf_embeddings = np.array([
            np.array(embedding, dtype=np.float32)
            for embedding in df['tfidf_embedding']
        ])
        bert_embeddings = np.array([
            np.array(embedding, dtype=np.float32)
            for embedding in df['bert_embedding']
        ])

        query_tfidf = generate_tfidf_embedding(query_text)
        query_bert = generate_bert_embedding(query_text)

        # Ensure the embeddings are not empty and have compatible dimensions
        if query_tfidf.size == 0 or tfidf_embeddings.size == 0:
            raise ValueError("TF-IDF embeddings are empty.")
        if query_bert.size == 0 or bert_embeddings.size == 0:
            raise ValueError("BERT embeddings are empty.")
        if query_tfidf.shape[1] != tfidf_embeddings.shape[1]:
            raise ValueError(f"Incompatible dimension for TF-IDF embeddings: query_tfidf.shape[1] = {query_tfidf.shape[1]}, tfidf_embeddings.shape[1] = {tfidf_embeddings.shape[1]}")
        if query_bert.shape[1] != bert_embeddings.shape[1]:
            raise ValueError(f"Incompatible dimension for BERT embeddings: query_bert.shape[1] = {query_bert.shape[1]}, bert_embeddings.shape[1] = {bert_embeddings.shape[1]}")

        tfidf_similarities = cosine_similarity(query_tfidf, tfidf_embeddings)
        bert_similarities = cosine_similarity(query_bert, bert_embeddings)

        combined_similarities = 0.3 * tfidf_similarities + 0.7 * bert_similarities
        ranked_indices = combined_similarities.argsort()[0][::-1]

        ranked_datasets = df.iloc[ranked_indices]

        # Add similarity scores to the DataFrame
        ranked_datasets['similarity_score'] = combined_similarities[0][ranked_indices]

        # Fetch metadata for the top results
        results = []
        for _, row in ranked_datasets.iterrows():
            dataset_id = row['dataset_id']
            similarity_score = row['similarity_score']

            metadata = Metadata.objects.filter(id=dataset_id).first()
            if metadata:
                results.append({
                    'id': metadata.id,
                    'title': metadata.title,
                    'description': metadata.description,
                    'url': metadata.url,
                    'size': metadata.size,
                    'format': metadata.format,
                    'similarity_score': similarity_score
                })
            else:
                logger.warning(f"Metadata not found for dataset ID {dataset_id}")

        return results

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise

# if __name__ == "__main__":
#     query_text = "Find datasets about e-commerce sales"
#     results = process_query(query_text)
#     print(results)
import os
import sys
import django
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Set up Django environment
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from recommendations.models import Metadata

# Fetch metadata
metadata = Metadata.objects.all().values('title', 'description')
df = pd.DataFrame(metadata)
df['combined_text'] = df['title'].fillna('') + ' ' + df['description'].fillna('')

# Create and save the TF-IDF vectorizer
vectorizer = TfidfVectorizer()
vectorizer.fit(df['combined_text'])
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
print("TF-IDF vectorizer saved as tfidf_vectorizer.pkl")
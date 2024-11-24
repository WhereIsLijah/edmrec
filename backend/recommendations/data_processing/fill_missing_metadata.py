import os
import tempfile
import pandas as pd
from sqlalchemy import create_engine, text
from transformers import pipeline
from kaggle.api.kaggle_api_extended import KaggleApi
from decouple import config
import logging
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration dynamically using `python-decouple`
DB_URL = config('DATABASE_URL')

if DB_URL.startswith('postgres://'):
    DB_URL = DB_URL.replace('postgres://', 'postgresql://', 1)

# Set up PostgreSQL connection
engine = create_engine(DB_URL)

# Initialize the NER model
ner_model = pipeline("ner", aggregation_strategy="simple")

# Initialize the summarizer model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Initialize Kaggle API
api = KaggleApi()
api.authenticate()

def extract_dataset_slug(url):
    """
    Extracts the dataset slug (username/dataset-name) from a Kaggle URL.
    """
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip('/').split('/')
    if len(path_parts) >= 2:
        return f"{path_parts[-2]}/{path_parts[-1]}"
    else:
        return None

def extract_text_from_dataset(directory):
    text_content = ""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv') or file.endswith('.txt'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        text_content += f.read()
                except Exception as e:
                    logger.error(f"Error reading file {file}: {e}")
    return text_content

def generate_metadata_using_ner(text):
    ner_results = ner_model(text)
    title = " ".join([res['word'] for res in ner_results if res['entity_group'] == 'TITLE'])
    description = " ".join([res['word'] for res in ner_results if res['entity_group'] == 'DESCRIPTION'])
    return title, description

def fetch_metadata_from_kaggle(dataset_slug):
    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Download the dataset
            api.dataset_download_files(dataset_slug, path=tmpdirname, unzip=True)
            # Extract text content from the dataset
            text_content = extract_text_from_dataset(tmpdirname)
            return text_content
    except Exception as e:
        logger.error(f"Error fetching dataset {dataset_slug}: {e}")
        return None

def process_missing_metadata(row):
    dataset_url = row['url']
    dataset_slug = extract_dataset_slug(dataset_url)

    generated_title, generated_description = row['title'], row['description']
    updated = False

    print(f"Processing dataset ID {row['id']}...")  # Debugging line

    # If title is missing, try to generate it using existing description
    if pd.isna(row['title']) or not row['title'].strip():
        ner_generated_title = generate_metadata_using_ner(row['description'])
        if ner_generated_title:
            generated_title = ner_generated_title
            print(f"Generated title using NER for dataset {row['id']}.")  # Debugging line
            updated = True

    # If description is missing, try to generate it using existing title
    if pd.isna(row['description']) or not row['description'].strip():
        ner_generated_description = generate_metadata_using_ner(row['title'])
        if ner_generated_description:
            generated_description = ner_generated_description
            print(f"Generated description using NER for dataset {row['id']}.")  # Debugging line
            updated = True

    if updated:
        return generated_title, generated_description
    else:
        return None, None

def fill_missing_metadata():
    """
    Fills missing titles and descriptions in the metadata database.
    """
    with engine.connect() as connection:
        trans = connection.begin()
        try:
            df = pd.read_sql("SELECT * FROM recommendations_metadata", connection)
            for index, row in df.iterrows():
                try:
                    title_missing = pd.isna(row['title']) or row['title'].strip() == ''
                    description_missing = pd.isna(row['description']) or row['description'].strip() == ''
                    
                    if title_missing or description_missing:
                        dataset_url = row['url']
                        dataset_slug = extract_dataset_slug(dataset_url)
                        if not dataset_slug:
                            logger.error(f"Could not extract dataset slug from URL: {dataset_url}")
                            continue
                        
                        if title_missing and not description_missing:
                            # Use the existing description to generate the title
                            generated_title, _ = generate_metadata_using_ner(row['description'])
                            row['title'] = generated_title if generated_title else row['title']
                        
                        if description_missing or (title_missing and description_missing):
                            # Fetch the content of the dataset to generate the description
                            text_content = fetch_metadata_from_kaggle(dataset_slug)
                            if text_content:
                                # Truncate text content to the maximum sequence length supported by the model
                                max_length = 1024
                                text_content = text_content[:max_length]
                                
                                generated_title, generated_description = generate_metadata_using_ner(text_content)
                                
                                if title_missing and generated_title:
                                    row['title'] = generated_title
                                    print(f"ID {row['id']} missing title, generated title: {row['title']}")
                                if description_missing and generated_description:
                                    row['description'] = generated_description
                                    print(f"ID {row['id']} missing description, generated description: {row['description']}")
                            else:
                                logger.warning(f"No headers or content found for dataset ID {row['id']}")
                    
                        update_query = text("""
                        UPDATE recommendations_metadata
                        SET title = :title, description = :description
                        WHERE id = :id
                        """)
                        connection.execute(update_query, {
                            'title': row['title'],
                            'description': row['description'],
                            'id': row['id']
                        })
                        print(f"Updated dataset ID {row['id']} with new metadata.")
                except Exception as e:
                    logger.error(f"Error processing dataset ID {row['id']}: {e}")

            trans.commit()
        except Exception as e:
            logger.error(f"Error during database operation: {e}")
            trans.rollback()

if __name__ == "__main__":
    fill_missing_metadata()
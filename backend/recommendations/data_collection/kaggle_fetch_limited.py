import os
import sys
import django
from datetime import datetime
import kaggle
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up Kaggle configuration
os.environ['KAGGLE_CONFIG_DIR'] = os.path.expanduser('~/.kaggle')

# Add Django project paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from recommendations.models import Metadata

# Authenticate Kaggle API
kaggle.api.authenticate()

def fetch_kaggle_metadata(search_term, max_pages=10):
    dataset_info = []
    page = 1

    while page <= max_pages:
        logger.info(f"Making API call to fetch datasets on page {page} for term '{search_term}'...")
        try:
            datasets = kaggle.api.dataset_list(search=search_term, page=page)
            if not datasets:
                logger.info(f"No more datasets found on page {page} for term '{search_term}'. Ending extraction.")
                break
        except Exception as e:
            logger.error(f"Error fetching dataset list on page {page} for term '{search_term}': {e}")
            break

        for dataset in datasets:
            dataset_ref = getattr(dataset, 'ref', None)
            dataset_title = getattr(dataset, 'title', None)
            dataset_subtitle = getattr(dataset, 'subtitle', None)
            dataset_size = getattr(dataset, 'size', None)
            dataset_format = getattr(dataset, 'fileType', None)
            
            if not dataset_ref:
                logger.warning("Dataset ref not found, skipping...")
                continue
            

            logger.info(f"Collecting metadata for dataset: {dataset_ref}")
            dataset_info.append({
                'title': dataset_title,
                'description': dataset_subtitle,
                'url': f'https://www.kaggle.com/datasets/{dataset_ref}',
                'size': dataset_size,
                'source': 'Kaggle',
                'format': dataset_format,
                'date_added': datetime.now(),
            })

        page += 1

    return dataset_info

def save_metadata_to_db(metadata):
    for data in metadata:
        format_value = data.get('format') or 'unknown'
        if not Metadata.objects.filter(url=data['url']).exists():
            Metadata.objects.create(
                title=data['title'],
                description=data['description'],
                url=data['url'],
                size=data['size'],
                source=data['source'],
                format=format_value, 
                created_at=data['date_added'],
                updated_at=data['date_added']
            )
    logger.info("Metadata saved to the database")

if __name__ == "__main__":
    search_terms = ['e-commerce', 'ecommerce']
    all_metadata = []

    for term in search_terms:
        metadata = fetch_kaggle_metadata(search_term=term, max_pages=10)
        all_metadata.extend(metadata)

    save_metadata_to_db(all_metadata)

import os
import sys
import django
from datetime import datetime
import kaggle
import json

os.environ['KAGGLE_CONFIG_DIR'] = os.path.expanduser('~/.kaggle')

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from recommendations.models import Metadata

kaggle.api.authenticate()

def fetch_kaggle_metadata(search_term='e-commerce'):
    dataset_info = []
    page = 1

    while True:
        print(f"Making API call to fetch datasets on page {page}...")
        try:
            datasets = kaggle.api.dataset_list(search=search_term, page=page)
            if not datasets:
                print(f"No more datasets found on page {page}. Ending extraction.")
                break
        except Exception as e:
            print(f"Error fetching dataset list on page {page}: {e}")
            break

        for dataset in datasets:
            dataset_ref = getattr(dataset, 'ref', None)
            dataset_title = getattr(dataset, 'title', None)
            dataset_subtitle = getattr(dataset, 'subtitle', None)
            dataset_size = getattr(dataset, 'size', None)
            if not dataset_ref:
                print("Dataset ref not found, skipping...")
                continue
            print(f"Fetching metadata for dataset: {dataset_ref}")
            try:
                dataset_files_response = kaggle.api.dataset_list_files(dataset_ref)
                dataset_files = getattr(dataset_files_response, 'files', None)
                if not dataset_files:
                    print(f"No files found for dataset {dataset_ref}")
                    continue
                file_formats = set([file.name.split('.')[-1] for file in dataset_files])

                dataset_info.append({
                    'title': dataset_title,
                    'description': dataset_subtitle,
                    'url': f'https://www.kaggle.com/datasets/{dataset_ref}',
                    'size': dataset_size,
                    'source': 'Kaggle',
                    'format': ', '.join(file_formats),
                    'date_added': datetime.now(),
                })
            except Exception as e:
                print(f"Error fetching files for dataset {dataset_ref}: {e}")

        page += 1

    return dataset_info

def save_metadata_to_db(metadata):
    for data in metadata:
        if not Metadata.objects.filter(url=data['url']).exists():
            Metadata.objects.create(
                title=data['title'],
                description=data['description'],
                url=data['url'],
                size=data['size'],
                source=data['source'],
                format=data['format'],
                created_at=data['date_added'],
                updated_at=data['date_added']
            )
    print("Metadata saved to the database")

if __name__ == "__main__":
    search_terms = ['e-commerce', 'ecommerce']
    all_metadata = []

    for term in search_terms:
        metadata = fetch_kaggle_metadata(search_term=term)
        all_metadata.extend(metadata)

    save_metadata_to_db(all_metadata)

# import os
# import sys
# import django
# import hashlib
# from datetime import datetime
# import kaggle

# # Ensure the kaggle.json file is in the correct directory
# os.environ['KAGGLE_CONFIG_DIR'] = os.path.expanduser('~/.kaggle')

# # Add the project root and backend directory to sys.path
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
# sys.path.append(project_root)
# sys.path.append(os.path.join(project_root, 'backend'))

# # Set up Django environment
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
# django.setup()

# from recommendations.models import Metadata # Adjust the import based on your project structure

# # Authenticate using kaggle.json
# kaggle.api.authenticate()

# def fetch_kaggle_metadata(search_term='e-commerce'):
#     dataset_info = []
#     page = 1
#     max_pages = 40  # Limit to 2 pages for now

#     while page <= max_pages:
#         print(f"Making API call to fetch datasets on page {page} for search term '{search_term}'...")
#         try:
#             datasets = kaggle.api.dataset_list(search=search_term, page=page)
#             if isinstance(datasets, str):
#                 print(f"Unexpected response: {datasets}")
#                 break
#             if not datasets:
#                 print(f"No more datasets found on page {page}. Ending extraction.")
#                 break
#         except Exception as e:
#             print(f"Error fetching dataset list on page {page}: {e}")
#             break

#         for dataset in datasets:
#             print(f"Fetching metadata for dataset: {dataset.ref}")
#             try:
#                 dataset_files_response = kaggle.api.dataset_list_files(dataset.ref)
#                 dataset_files = getattr(dataset_files_response, 'files', None)
#                 if not dataset_files:
#                     print(f"No files found for dataset {dataset.ref}")
#                     continue
#                 if isinstance(dataset_files, str):
#                     print(f"Unexpected response for dataset files: {dataset_files}")
#                     continue
#                 file_formats = set([file.name.split('.')[-1] for file in dataset_files])

#                 dataset_info.append({
#                     'title': dataset.title,
#                     'description': dataset.subtitle,
#                     'url': f'https://www.kaggle.com/{dataset.ref}',
#                     'size': dataset.size,
#                     'source': 'Kaggle',
#                     'format': ', '.join(file_formats),
#                     'date_added': datetime.now()
#                 })
#             except Exception as e:
#                 print(f"Error fetching files for dataset {dataset.ref}: {e}")

#         page += 1

#     return dataset_info
#     dataset_info = []
#     page = 1

#     while page <= max_pages:
#         print(f"Making API call to fetch datasets on page {page} for search term '{search_term}'...")
#         try:
#             datasets = kaggle.api.dataset_list(search=search_term, page=page)
#             if isinstance(datasets, str):
#                 print(f"Unexpected response: {datasets}")
#                 break
#             if not datasets:
#                 print(f"No more datasets found on page {page}. Ending extraction.")
#                 break
#         except Exception as e:
#             print(f"Error fetching dataset list on page {page}: {e}")
#             break

#         for dataset in datasets:
#             print(f"Fetching metadata for dataset: {dataset.ref}")
#             try:
#                 dataset_files_response = kaggle.api.dataset_list_files(dataset.ref)
#                 dataset_files = getattr(dataset_files_response, 'files', None)
#                 if not dataset_files:
#                     print(f"No files found for dataset {dataset.ref}")
#                     continue
#                 file_formats = set([file.name.split('.')[-1] for file in dataset_files])

#                 dataset_info.append({
#                     'title': dataset.title,
#                     'description': dataset.subtitle,
#                     'url': f'https://www.kaggle.com/{dataset.ref}',
#                     'size': dataset.size,
#                     'source': 'Kaggle',
#                     'format': ', '.join(file_formats),
#                     'date_added': datetime.now()
#                 })
#             except Exception as e:
#                 print(f"Error fetching files for dataset {dataset.ref}: {e}")

#         page += 1

#     return dataset_info

# def save_metadata_to_db(metadata):
#     for data in metadata:
#         # Check if the dataset already exists in the database using the URL
#         if not Metadata.objects.filter(url=data['url']).exists():
#             Metadata.objects.create(
#                 title=data['title'],
#                 description=data['description'],
#                 url=data['url'],
#                 size=data['size'],
#                 source=data['source'],
#                 format=data['format'],
#                 created_at=data['date_added'],
#                 updated_at=data['date_added']
#             )
#     print("Metadata saved to the database")

# if __name__ == "__main__":
#     search_terms = ['e-commerce', 'ecommerce']
#     all_metadata = []

#     for term in search_terms:
#         metadata = fetch_kaggle_metadata(search_term=term)
#         all_metadata.extend(metadata)

#     save_metadata_to_db(all_metadata)
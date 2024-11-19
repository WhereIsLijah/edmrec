
# EDMRec: E-commerce Dataset Mining Recommendation System

**Author**: Ayomide Elijah Oduba  
**University**: University of Windsor  
**Date**: November 14, 2024

## 📖 Overview

**EDMRec** is a hybrid recommendation system designed to enhance dataset recommendations for e-commerce by leveraging advanced Natural Language Processing (NLP) techniques. The system combines **Named Entity Recognition (NER)** and **BERT embeddings** for semantic understanding with **TF-IDF** for keyword relevance, delivering accurate and contextually relevant dataset recommendations.

The backend is built with **Django**, and the frontend is built with **React** to provide a seamless and interactive user experience.

---

## 🔑 Key Features

- **Metadata Enrichment**: Enhances incomplete metadata using Named Entity Recognition (NER).
- **Hybrid Recommendation Model**:
  - Combines **TF-IDF** for keyword-based relevance.
  - Integrates **BERT embeddings** for semantic relevance.
- **Layered Architecture**:
  - **Data Collection**: Standardizes and extracts metadata.
  - **Data Processing**: Validates and enriches metadata.
  - **Query Processing**: Ranks datasets based on relevance.

---

## 🛠️ System Components

1. **Data Collection Layer**:
   - Sources: Kaggle, Google Dataset Search, public repositories, and APIs.
   - Outputs standardized metadata stored in a unified schema.

2. **Data Processing Layer**:
   - Techniques: Named Entity Recognition (NER), metadata validation.
   - Outputs validated metadata with improved quality.

3. **Query Processing Layer**:
   - Methods: TF-IDF, BERT embeddings, cosine similarity.
   - Outputs ranked datasets based on user query relevance.

4. **Frontend and Backend**:
   - **Frontend**:
     - Built with React to provide an intuitive user interface for interacting with the recommendation system.
   - **Backend**:
     - Built with Django to handle API calls, metadata storage, and query processing.

---

## 🚀 Installation

### Prerequisites

- **Python** (>= 3.8)
- **PostgreSQL** (for metadata storage)
- Required Libraries:
  - TensorFlow or PyTorch (for BERT embeddings)
  - scikit-learn (for TF-IDF)
  - spaCy (for NER)
  - SQLAlchemy (for database interaction)
- Django (for backend API development)
- Node.js and npm (for React frontend)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/edmrec.git
   cd edmrec
   ```

## Backend Setup

2. **Navigate to the backend folder**:
   ```bash
   cd backend
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the PostgreSQL database**:

   Create a database named `edmrec_db`. Use the following schema for the `ecommerce_datasets` table:

   ```sql
   CREATE TABLE ecommerce_datasets (
       id SERIAL PRIMARY KEY,
       title TEXT,
       description TEXT,
       URL TEXT,
       size TEXT,
       format TEXT,
       date_added TIMESTAMP,
       date_updated TIMESTAMP,
       tfidf_embeddings BYTEA,
       bert_embeddings BYTEA,
       source TEXT
   );
   ```

5. **Run the backend server**:
   ```bash
   python manage.py runserver
   ```

## Frontend Setup

1. **Navigate to the frontend folder**:
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the React development server**:
   ```bash
   npm start
   ```

4. **Access the React frontend**:  
   Open your browser and navigate to [http://localhost:3000](http://localhost:3000) to interact with the system.

---

## Run the System

1. Populate the database with metadata using the provided scripts.
2. Use the React frontend to query and interact with the system.

---

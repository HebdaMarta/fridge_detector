# 🥗 AI Fridge Chef

AI Fridge Chef is an application that analyzes a photo of a refrigerator, detects available food products using a vision-language model, allows the user to verify detected ingredients, and generates personalized recipe suggestions based on available ingredients and user preferences.

---

# Features

* 📸 Refrigerator photo analysis
* 🤖 Product detection using a multimodal AI model (Qwen2.5-VL)
* ✅ Ingredient verification by the user
* 🔍 Recipe retrieval using vector search (RAG)
* 🖥 Modern Streamlit user interface
* 🔒 Fully local execution (no cloud APIs required)

---

# Architecture

The application consists of five main stages:

## 1. Image Upload

The user uploads a refrigerator photo through the Streamlit frontend.

Example:

* vegetables
* fruits
* dairy products
* eggs
* sauces
* packaged food

The image is sent to the FastAPI backend.

---

## 2. Refrigerator Analysis

The uploaded image is analyzed by the multimodal model:

Qwen2.5-VL-7B

The model receives:

* refrigerator image
* detection prompt

Example prompt:

"Analyze this refrigerator image. List every visible food product. Estimate quantities when possible. Return JSON only."

Example output:

```json
{
  "products": [
    {
      "name": "Tomatoes",
      "quantity": "5",
      "confidence": 90
    },
    {
      "name": "Eggs",
      "quantity": "6",
      "confidence": 95
    }
  ]
}
```

---

## 3. Product Verification

Detected products are divided into two groups:

### Confirmed Products

Products with confidence above the threshold.

Example:

* Tomatoes
* Eggs
* Milk

### Possible Products

Products with lower confidence.

Example:

* Cheese
* Strawberries

The user can:

* remove incorrectly detected products
* add uncertain products
* decide which ingredients should be used in recipe generation

This significantly improves final recipe quality.

---

## 4. Recipe Retrieval (RAG)

The application uses PostgreSQL with the pgvector extension as a vector database.
The distiluse-base-multilingual-cased-v2 model is used to convert recipes and user queries into vector embeddings
Pipeline:

User Query
↓
distiluse-base-multilingual-cased-v2
↓
Similarity search (via pgvector in PostgreSQL)
↓
Top 3 matching recipes

Example query:

```text
Tomatoes Eggs Milk Healthy dinner
```

The vector database returns the most relevant recipes.

---

## 5. Recipe Generation

The application uses PostgreSQL with the pgvector extension as the source of truth for all recipes.
Retrieval model:

distiluse-base-multilingual-cased-v2

Inputs:

* selected ingredients: The list of products verified from your refrigerator
* user preferences: Specific constraints (e.g., "healthy," "quick")
* retrieved recipes: Structured data pulled directly from the PostgreSQL database

Example preference:

```text
Healthy dinner with vegetables
```

The model generates:

```json
{
  "recipes": [
    {
      "title": "Tomato Omelette",
      "Calories": "450 kcal",
      "Ingredients": "pasta shapes, avocado",
      "Recipe steps": "Cook the pasta for 10 mins in salted boiling water until al dente"
    }
  ]
}
```

---

# Technology Stack

## Frontend

* Streamlit

## Backend

* FastAPI

## Computer Vision

* Qwen2.5-VL-7B (Ollama 4-bit version)


## Retrieval-Augmented Generation

* PostgreSQL with pgvector
* Sentence Transformers
* distiluse-base-multilingual-cased-v2

## Data Processing

* Python 3.12

---

# Project Structure

```text
fridge_detection/

├── backend/
│   ├── __init__.py
│   ├── api.py
│   ├── detector.py
│   ├── helper.py
│   ├── main_embedding.py
│   ├── sql_engine_embedding.py
│   └── schemas.py
│
├── frontend/
│   └── streamlit_app.py
│
├── data/
│   ├── uploads/
│   └── recipes.json
│
├── vectorscale_db/
│   ├── initdb/
│   └── docker-compose.yml
│
└── README.md
```

---

# Installation

## Clone repository

```bash
git clone <repository-url>
cd fridge_detection
```

## Install dependencies

```bash
uv sync
```

---

# Ollama Models

Install Ollama:

https://ollama.com

Pull required models:

```bash
ollama pull qwen2.5vl:7b
```

Verify:

```bash
ollama list
```

Expected:

```text
qwen2.5vl:7b
```

---

# Running the Application

## Start Ollama

```bash
ollama serve
```
## Start Vector Database

```bash
cd vectorscale_db
docker compose up -d
```

## Upload Recipes as JSON file and locate in the data/ directory
```bash
uv run recipes_upload.py
```
---
## Initialize Database and Generate Embeddings on the first run

```bash
uv run recipes_data_embedding.py
```

## Verify your Database

```bash
uv run python -c "from backend.sql_engine_embedding import engine; from backend.main_embedding import Recipes; from sqlalchemy.orm import Session; session = Session(engine); print(f'Database is active. Total recipes found: {session.query(Recipes).count()}')"
```

## Start FastAPI backend

```bash
uv run uvicorn backend.api:app --reload
```

Backend:

```text
http://localhost:8000
```

---

## Start Streamlit frontend

Open a second terminal:

```bash
uv run streamlit run frontend/streamlit_app.py
```

Frontend:

```text
http://localhost:8501
```

---

# Workflow

```text
Upload refrigerator photo
          ↓
Qwen2.5-VL product detection
          ↓
Confidence filtering
          ↓
User verification
          ↓
Recipe retrieval from PostgreSQL
          ↓
Display recipe steps
```

---

# Future Improvements

* Recipe images generated with AI
* Barcode recognition
* Product expiration tracking
* Nutrition estimation
* Shopping list generation
* Voice assistant
* Cloud deployment
* User accounts and fridge history

---

# License

MIT License
GNU Free Documentation License 1.3
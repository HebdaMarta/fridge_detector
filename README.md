# 🥗 AI Fridge Chef

AI Fridge Chef is an application that analyzes a photo of a refrigerator, detects available food products using a vision-language model, allows the user to verify detected ingredients, and generates personalized recipe suggestions based on available ingredients and user preferences.

---

# Features

* 📸 Refrigerator photo analysis
* 🤖 Product detection using a multimodal AI model (Qwen2.5-VL)
* ✅ Ingredient verification by the user
* 🔍 Recipe retrieval using vector search (RAG)
* 🍳 Personalized recipe generation using a local LLM
* 🖥 Modern Streamlit user interface
* 🔒 Fully local execution (no cloud APIs required)

---

# Architecture

The application consists of four main stages:

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

The application uses ChromaDB as a vector database.

Recipe descriptions are embedded using:

all-MiniLM-L6-v2

Pipeline:

User ingredients
↓
Embedding generation
↓
Similarity search
↓
Top 3 matching recipes

Example query:

```text
Tomatoes Eggs Milk Healthy dinner
```

The vector database returns the most relevant recipes.

---

## 5. Recipe Generation

Retrieved recipes are passed to a local LLM.

Current model:

Phi-3

Inputs:

* selected ingredients
* user preferences
* retrieved recipes from ChromaDB

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
      "description": "Healthy omelette with vegetables.",
      "time": "15 min",
      "difficulty": "easy"
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

* Qwen2.5-VL-7B
* Ollama

## Retrieval-Augmented Generation

* ChromaDB
* Sentence Transformers
* all-MiniLM-L6-v2

## LLM

* Phi-3
* Ollama

## Data Processing

* Python 3.12

---

# Project Structure

```text
fridge_detection/

├── backend/
│   ├── api.py
│   ├── detector.py
│   ├── helper.py
│   ├── rag.py
│   ├── llm.py
│   └── schemas.py
│
├── frontend/
│   └── streamlit_app.py
│
├── data/
│   ├── uploads/
│   └── chroma/
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

## Create virtual environment

```bash
uv venv
```

## Activate environment

Windows:

```bash
.venv\Scripts\activate
```

Linux / Mac:

```bash
source .venv/bin/activate
```

## Install dependencies

```bash
uv pip install -r requirements.txt
```

---

# Ollama Models

Install Ollama:

https://ollama.com

Pull required models:

```bash
ollama pull qwen2.5vl:7b
ollama pull phi3
```

Verify:

```bash
ollama list
```

Expected:

```text
qwen2.5vl:7b
phi3
```

---

# Running the Application

## Start Ollama

```bash
ollama serve
```

---

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
streamlit run frontend/streamlit_app.py
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
Recipe retrieval from ChromaDB
          ↓
Recipe generation with Phi-3
          ↓
Display recipe suggestions
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

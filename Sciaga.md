## Poniższy opis dotyczy dwóch wersji projektu, main oraz branch wersja_z_embeddingiem

## Pobieranie bazy danych
uv run python scripts/download_data.py

## Zarządzanie środowiskiem
uv sync



# W przypadku wersji_z_embeddingiem: 
## wysyłanie do repozytorium na github
git push -u origin wersja_z_embeddingiem
## pobieranie z repozytorium na github
git clone -b wersja_z_embeddingiem https://github.com/DonPedrodePommidore/Aplikacja_przepisy.git
## Uruchomienie kontenera
docker compose up -d
## Połączenie z bazą
psql -d "postgres://postgres:password@localhost:5555/postgres"
## Dodanie pakietu vector i vectorscale
CREATE EXTENSION IF NOT EXISTS vectorscale CASCADE
## Sprawdzenie czy plpsqscl, timescaledb, timescaledb)toolkit, vector, vectorscale jest na liście po dodaniu pakietu
\dx
## odpalenie embeddingu danych celem przygotowania bazy
uv run recipes_data_embedding.py
## wysyłanie zapytania odnośnie przepisu, konsola ma zwrócić przepis
uv run testing_queries_recipes_embedding.py


# W przypadku wersji main (bez embeddingu)
python init_db.py
## Instalacja fastapi uvicorn
uv add fastapi uvicorn
## W przypadku wersji main (bez embeddingu): migracja danych z json do db
python init_db.py
## Uruchamianie servera API
uvicorn main:app --reload
Nasłuch pod adresem http://127.0.0.1:8000
Swagger pod adresem http://127.0.0.1:8000/docs

## Przykładowe żądanie w Swaggerze
{
  "ingredients": [
    "cream",
    "milk",
    "eggs"
  ]
}
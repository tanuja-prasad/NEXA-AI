# NEXA — AI

## Folder structure

- `frontend/app.py` — existing Streamlit user interface.
- `backend/api.py` — FastAPI HTTP API.
- `backend/` — RAG pipeline, graph workflow, memory, retrieval, scraping, vector DB and other backend modules/data.
- `backend/.env.example` — safe template for environment configuration.

## Run

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r backend/requirements.txt`
3. Copy `backend/.env.example` to `backend/.env` and fill in your own credentials.
4. Run the Streamlit frontend from the project root:
   `streamlit run frontend/app.py`
5. To run the FastAPI backend, from the project root:
   `uvicorn api:app --app-dir backend --reload`



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

Note: this is a structural separation of the existing project. The UI is Streamlit, not a separate React/HTML frontend. The original `.env`, Git history, and virtual environment were intentionally excluded to avoid exposing secrets and bulky machine-specific dependencies. Review `.env.example` and add any additional variables required by your setup.

# NEXA Frontend

The current frontend is a Streamlit UI (`app.py`). It imports backend modules from `../backend`.

From the project root, install backend dependencies and run:

```bash
pip install -r backend/requirements.txt
streamlit run frontend/app.py
```

Configure your own credentials in `backend/.env` (start from `.env.example`). Do not share secrets.

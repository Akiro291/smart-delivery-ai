cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install fastapi uvicorn pydantic-settings python-dotenv
uvicorn app.main:app --host 0.0.0.0 --port 8000
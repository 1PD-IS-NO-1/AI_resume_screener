# Backend
FROM python:3.9-slim as backend

WORKDIR /app
COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend .
COPY ./model /app/model
COPY ./Resume /app/Resume

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# Frontend
FROM python:3.9-slim as frontend

WORKDIR /app
COPY ./frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./frontend .

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
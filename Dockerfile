FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 8000 8501

CMD ["sh", "-c", "uvicorn src.api:app --host 0.0.0.0 --port 8000 & streamlit run src/main.py --server.port 8501"]
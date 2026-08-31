FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY 02_en_marcha/servicio_contenedor.py .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD python -c "from urllib.request import urlopen; urlopen('http://127.0.0.1:8000/salud', timeout=2)"

CMD ["uvicorn", "servicio_contenedor:app", "--host", "0.0.0.0", "--port", "8000"]

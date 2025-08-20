# # services/tpms-service/Dockerfile
# FROM python:3.11-slim
# WORKDIR /app
# COPY . /app
# RUN apt-get update && apt-get install -y build-essential --no-install-recommends && rm -rf /var/lib/apt/lists/*
# RUN pip install --no-cache-dir -r requirements.txt
# ENV PYTHONUNBUFFERED=1
# EXPOSE 8001
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]


FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]

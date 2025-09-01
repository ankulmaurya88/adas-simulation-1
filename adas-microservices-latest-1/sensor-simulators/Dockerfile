FROM python:3.11-slim
WORKDIR /app
COPY app/ ./app
RUN pip install paho-mqtt
CMD ["python", "app/simulator.py"]

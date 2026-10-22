FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# app:app 대신 main:app으로 지정합니다.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]

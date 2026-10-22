FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# main.py 파일을 사용하므로 main:app으로 지정합니다.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]

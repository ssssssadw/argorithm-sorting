# 공식 파이썬 슬림 이미지 사용
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Gunicorn 서버를 이용해 Flask 앱 실행 (포트 8080 개방)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]

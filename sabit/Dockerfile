# 파이썬 가벼운 공식 이미지 사용
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 패키지 목록 복사 및 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Cloud Run 포트 환경변수 설정
ENV PORT=8080

# Gunicorn 서버를 통해 플라스크 앱 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]

# 파이썬 공식 슬림 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 파일 복사 및 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY main.py .

# 클라우드 런 포트 환경변수 설정 및 Gunicorn 서버 실행
ENV PORT=8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main.py:app"]

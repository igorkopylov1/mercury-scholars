FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

# Скопируйте сертификаты в контейнер
COPY /certificates ./certificates/

COPY app/ ./app/
COPY bin/ ./bin/

CMD ["python3", "-m", "bin.__main__"]
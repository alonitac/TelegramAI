FROM python:3.8.12-slim-buster

WORKDIR /TelegramAI
COPY . .
RUN pip install -r requirements.txt

CMD ["python3", "app.py"]
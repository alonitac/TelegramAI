FROM python:3.8.12-slim-buster


COPY app.py /
COPY mainApp.py /
COPY .telegramToken /
COPY requirements.txt /tmp/
COPY utils.py /
RUN pip install --requirements /tmp/requirements.txt


CMD ["python3", "app.py"]
FROM python:3.8.12-slim-buster
WORKDIR .
COPY . .
#ENV MAIN_APP=app.py
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"]
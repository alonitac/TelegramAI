FROM python:3.8.12-slim-buster
WORKDIR .
COPY . .
#ENV MAIN_APP=app.py
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN sleep 240
CMD ["python3", "new.py"]
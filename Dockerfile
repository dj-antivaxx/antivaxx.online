FROM python:latest

WORKDIR /home/src

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src /home/src

CMD ["python", "app.py"]

FROM python:3.9

WORKDIR ./Orator

ADD . .

RUN pip install -r requirements.txt

CMD ["python", "./main.py"]
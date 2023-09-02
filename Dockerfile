FROM python:3.9

WORKDIR ./Orator

ADD . .

RUN apt-get update
RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y
RUN pip install pyaudio
RUN pip install -r requirements.txt

CMD ["python", "./main"]
FROM python:3.7-buster
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["sudo", "apt-get", "update"]
CMD ["sudo", "apt-get", "install", "libsndfile1", "-y"]

EXPOSE 5050
CMD ["python", "tasks/lightspeech_inference.py", "--config configs/tts/lj/lightspeech.yaml", "--exp_name lightspeech", "--inference_text inference_text.txt"]
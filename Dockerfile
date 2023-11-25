FROM cnstark/pytorch:2.0.1-py3.10.11-ubuntu22.04

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN mkdir -p /app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD streamlit run app.py

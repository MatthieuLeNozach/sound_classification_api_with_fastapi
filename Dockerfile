# CAUTION: ADD THE .environment FOLDER TO A .dockerignore FILE
# TO ENSURE THAT THE ENVIRONMENT VARIABLES AREN'T COPIED IN THE IMAGE

FROM python:3.10

# Install necessary packages for audio file handling
RUN apt-get update && \
    apt-get install -y libsndfile1 ffmpeg

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#CMD ["uvicorn", "--reload", "--host", "${HOST}", "--port", "${PORT}", "${APP_MODULE}"]

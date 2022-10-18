FROM python:3.8

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED 1

# Create and change to the app directory.
WORKDIR /usr/src/app


COPY requirements.txt ./


RUN pip install -U "discord.py"
RUN pip install -r requirements.txt

COPY . ./

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app


# RUN apt-get update && apt-get install -y google-api-python-client google-auth-httplib2 google-auth-oauthlib

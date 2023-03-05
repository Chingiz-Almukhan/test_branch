FROM python:3.9
WORKDIR /app
RUN apt-get update -y
RUN apt-get upgrade -y
COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./source ./source
COPY ./entrypoint.sh ./
CMD ["./entrypoint.sh"]
# CMD gunicorn -w 3 --chdir ./source quantum.wsgi --bind 0.0.0.0:8000
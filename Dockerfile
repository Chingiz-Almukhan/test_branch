FROM python:3.9.10
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt
COPY . .
EXPOSE 8000

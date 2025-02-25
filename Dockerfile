#Python Docker Image
FROM python:3.11

RUN apt-get update && \
    apt-get install -y
RUN apt-get install apache2-dev -y && apt install unixodbc -y
RUN pip install --upgrade pip

#Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PGSSLCERT /tmp/postgresql.crt

RUN mkdir /code
WORKDIR /code
COPY . /code

#Install dependencies

COPY requirements.txt /code/
RUN pip install -r requirements.txt

#Run server in Dev (local machine only)
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
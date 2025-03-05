# #Python Docker Image
# FROM python:3.11

# RUN apt-get update && \
#     apt-get install -y
# RUN apt-get install apache2-dev -y && apt install unixodbc -y
# RUN pip install --upgrade pip

# #Environment Variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# ENV PGSSLCERT /tmp/postgresql.crt

# RUN mkdir /code
# WORKDIR /code
# COPY . /code

# #Install dependencies

# COPY requirements.txt /code/
# RUN pip install -r requirements.txt

# #Run server in Dev (local machine only)
# EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM ubuntu:22.04


ARG BASE_DIR=/var/www
ARG WEBSITE_NAME=redepplan
ENV WEBSITE_NAME=${WEBSITE_NAME}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_DEVELOPMENT='true'
ENV DJANGO_SETTINGS_MODULE='redepplan.settings'

# Add apache2, mod_wsgi, python3.8 libraries
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install apache2 -y && DEBIAN_FRONTEND=noninteractive apt-get install apache2-dev -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install libapache2-mod-wsgi-py3 -y
RUN apt-get install build-essential -y
RUN apt-get install libssl-dev -y
RUN apt-get install libffi-dev -y
RUN apt-get install python3.10-dev  -y
RUN apt-get install python3.10 -y
RUN apt-get install python3.10-venv -y
RUN apt-get install python3-pip -y
RUN apt-get install vim -y
RUN apt-get install sudo -y
RUN apt-get install w3m -y\
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

# Expose port 80 on the container
EXPOSE 80
# Make directory for base_site
RUN mkdir -p ${BASE_DIR}/${WEBSITE_NAME}

ENTRYPOINT ["/bin/bash", "/var/www/startup.sh"]
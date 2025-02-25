# FROM httpd:2.4
# RUN apt-get update && apt-get install -y
# RUN apt-get install -y python3.10 && apt-get install -y python3-pip && apt install python3-venv -y
# RUN apt install libapache2-mod-wsgi-py3 -y

# RUN pip install --upgrade pip --break-system-packages
# RUN pip install --upgrade setuptools --break-system-packages
# RUN pip install unroll --break-system-packages
# RUN pip install ez_setup --break-system-packages
# RUN easy_install -U setuptools

# RUN pip install mod-wsgi==5.0.2 --break-system-packages

FROM ubuntu:18.04


ARG BASE_DIR=/var/www
ARG WEBSITE_NAME=redepplan
ENV WEBSITE_NAME=${WEBSITE_NAME}

# Add apache2, mod_wsgi, python3.6 libraries
RUN apt-get update && apt-get install -y apache2 \
    libapache2-mod-wsgi-py3 \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3.6-dev \
    python3.6 \
    python3.6-venv \
    python3-pip \
    vim \
    sudo \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf
# Expose port 80 on the container
EXPOSE 80
# Make directory for base_site
RUN mkdir ${BASE_DIR}/${WEBSITE_NAME}

CMD sudo apache2ctl -D FOREGROUND
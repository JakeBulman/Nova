#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Run a case command
case $1 in
    server)
    # Pull in Docker env
    WEBSITE_BASE_NAME="$(printenv WEBSITE_NAME)"
    BASE_PATH=/var/www/${WEBSITE_BASE_NAME}
    #install requirements
    sudo pip install -r $BASE_PATH/requirements.txt
    # Change to $BASE_PATH
    cd $BASE_PATH
    # Startup apache2 server
    sudo groupadd varwwwusers
    sudo adduser www-data varwwwusers
    sudo chgrp -R varwwwusers /var/www/
    sudo chmod -R 770 /var/www/
    echo "export DJANGO_ENV=${DJANGO_ENV}" >> /etc/environment
    echo "Starting Apache"
    sudo python3 manage.py collectstatic --no-input
    sudo apache2ctl -D FOREGROUND
    echo "Apache started"
    ;;

esac
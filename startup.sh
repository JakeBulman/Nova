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
    ENV_VAR_TEST="$(printenv DJANGO_DEVELOPMENT)"
    echo $ENV_VAR_TEST
    sudo apache2ctl -D FOREGROUND
    ;;

esac
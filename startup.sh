#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Run a case command
case $1 in
    server)
    # Pull in Docker env
    WEBSITE_BASE_NAME="$(printenv WEBSITE_NAME)"
    BASE_PATH=/var/www/${WEBSITE_BASE_NAME}

    # Check if requirements.txt exists, and there is no env already built
    # if [ -e $BASE_PATH/requirements.txt ] && [ ! -d $BASE_PATH/env ]; then
    #     # sudo rm /usr/bin/python3
    #     # sudo ln -s python3.8 /usr/bin/python3
    #     sudo pip3 install virtualenv
    #     cd $BASE_PATH
    #     virtualenv -p $(which python3) env
    #     source $BASE_PATH/env/bin/activate
    sudo pip install -r $BASE_PATH/requirements.txt
    #     else
    #         source $BASE_PATH/env/bin/activate
    # fi
    # Change to $BASE_PATH
    cd $BASE_PATH
    # Startup apache2 server
    sudo apache2ctl -D FOREGROUND
    ;;

esac
#!/usr/bin/env bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DOCKER_IMAGE="gitlab.devartis.com:4567/devops/simple-deploy:0.1-new-hope"
if [[ -z "$SSH_PRIVATE_KEY" || -z "$DJANGO_SECRET_KEY" ]]; then
    echo "Variables 'SSH_PRIVATE_KEY', 'DJANGO_SECRET_KEY' must be set";
    exit 1;
fi

if [[ -z "$HOST_LIMIT" ]]; then
    HOST_LIMIT="testing"
    echo "WARNING: Variables 'HOST_LIMIT' must be set. Default: testing";
fi

if [[ -z "$CHECKOUT_BRANCH" ]]; then
    CHECKOUT_BRANCH="master"
    echo "WARNING: Variables 'CHECKOUT_BRANCH' must be set. Default: testing";
fi

docker run --rm -v $DIR:/config/ -e SSH_PRIVATE_KEY="$SSH_PRIVATE_KEY" -e HOSTS_FILE_PATH=/config/hosts \
    -e REPO_URL="git@gitlab.devartis.com:thawk/intrepidboats.git" -e SETTINGS_FILE=intrepidboats.settings.production \
    -e APPLICATION_ENV_FILE=intrepidboats/settings/.env -e CHECKOUT_BRANCH="$CHECKOUT_BRANCH" \
    -e DJANGO_SECRET_KEY="$DJANGO_SECRET_KEY" -e DJANGO_WSGI=intrepidboats.wsgi \
    -e HOST_LIMIT="$HOST_LIMIT" -e TAGS="quickly" $DOCKER_IMAGE


#!/bin/bash

cd $(dirname "$0")/strato-certbot
git pull
cd ..
. $(dirname "$0")/../.env
certbot certonly --server https://acme-v02.api.letsencrypt.org/directory -d "*.${WILDCARD_DOMAIN}" --email "$MY_MAIL" --preferred-challenges dns --manual --config-dir $(dirname "$0")/letsencrypt --work-dir $(dirname "$0")/letsencrypt --logs-dir$(dirname "$0")/letsencrypt --manual-auth-hook $(dirname "$0")/certbotWrapperRenew.sh --manual-cleanup-hook $(dirname "$0")/certbotWrapperClean.sh
docker rm -f nginx
docker-compose --env-file $(dirname "$0")/../.env up -d
#!/bin/sh
#Set the language
set -e
export LANG="en_US.UTF-8"
. ../.env


curl -X POST --insecure -H "Content-Type: application/json" -d \
  '{"message": "Start '"$TIMESTAMP"' Backup for Databases", "number": "'"$SIGNAL_SOURCE_NUMBER"'", "recipients": ["'"$SIGNAL_TARGET_NUMBER"'"]}' \
  'https://signal.home/v2/send'



BACKUPDIR=${MYSQL_BACKUP_DIR}
if [ ! -d $BACKUPDIR ]; then
        mkdir -p $BACKUPDIR
fi

# Timestamp definition for the backupfiles (example: $(date +"%Y%m%d%H%M") = 20200124-2034)
TIMESTAMP=$(date +"%Y%m%d%H%M")
CONTAINER="mariadb"
MYSQL_DATABASE="nextcloud"
docker exec -e MYSQL_DATABASE=$MYSQL_DATABASE  \
        ${CONTAINER} /usr/bin/mysqldump -u dump $MYSQL_DATABASE \
        | gzip > $BACKUPDIR/${CONTAINER}-$MYSQL_DATABASE-$TIMESTAMP.sql.gz


curl -X POST --insecure -H "Content-Type: application/json" -d \
  '{"message": "Finished Backup for Databases", "number": "'"$SIGNAL_SOURCE_NUMBER"'", "recipients": ["'"$SIGNAL_TARGET_NUMBER"'"]}' \
  'https://signal.home/v2/send'


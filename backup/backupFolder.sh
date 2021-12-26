#!/bin/sh
set -x
runBackup() {
  SOURCE=$1
  TARGET=$2
  curl -X POST --insecure -H "Content-Type: application/json" -d \
    '{"message": "Starting sync of data $SOURCE to $TARGET", "number": "'"$SIGNAL_SOURCE_NUMBER"'", "recipients": ["'"$SIGNAL_TARGET_NUMBER"'"]}' \
  'https://signal.home/v2/send'
  rsync -a "$SOURCE" "$TARGET"
  curl -X POST --insecure -H "Content-Type: application/json" -d \
    '{"message": "Finished sync of docker data $SOURCE to $TARGET", "number": "'"$SIGNAL_SOURCE_NUMBER"'", "recipients": ["'"$SIGNAL_TARGET_NUMBER"'"]}' \
  'https://signal.home/v2/send'
}

(
  set -e
  export LANG="en_US.UTF-8"
  . $(dirname "$0")/../.env
  SOURCE=$1
  TARGET=$2
  runBackup "$SOURCE" "$TARGET"
)

if [ $? -ne 0 ]; then
  curl -X POST --insecure -H "Content-Type: application/json" -d \
    '{"message": "Failure during docker sync  $SOURCE to $TARGET", "number": "'"$SIGNAL_SOURCE_NUMBER"'", "recipients": ["'"$SIGNAL_TARGET_NUMBER"'"]}' \
  'https://signal.home/v2/send'
fi

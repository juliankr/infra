set -e
export LANG="en_US.UTF-8"
. $(dirname "$0")/../.env

$(dirname "$0")/strato-certbot/cleanup-hook.py "$@"

rm $(dirname "$0")/strato-certbot/strato-auth.json

curl -X POST --insecure -H "Content-Type: application/json" -d \
  '{"message": "Finished '"$TIMESTAMP"' setup strato for new cert", "number": "'"$SIGNAL_SOURCE_NUMBER"'", "recipients": ["'"$SIGNAL_TARGET_NUMBER"'"]}' \
  "https://signal.${WILDCARD_DOMAIN}/v2/send"
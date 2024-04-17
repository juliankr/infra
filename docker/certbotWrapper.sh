set -e
export LANG="en_US.UTF-8"
. $(dirname "$0")/../.env


curl -X POST --insecure -H "Content-Type: application/json" -d \
  '{"message": "Start '"$TIMESTAMP"' setup strato for new cert", "number": "'"$SIGNAL_SOURCE_NUMBER"'", "recipients": ["'"$SIGNAL_TARGET_NUMBER"'"]}' \
  'https://signal.home/v2/send'


echo '{
  "api_url": "https://www.strato.de/apps/CustomerService",
  "username": "'$STRATO_USER'",
  "password": "'$STRATO_PASSWORD'",
  "waiting_time": 60
}' > $(dirname "$0")/strato-certbot/strato-auth.json

$(dirname "$0")/strato-certbot/auth-hook.py "$@"

rm $(dirname "$0")/strato-certbot/strato-auth.json

curl -X POST --insecure -H "Content-Type: application/json" -d \
  '{"message": "Finished '"$TIMESTAMP"' setup strato for new cert", "number": "'"$SIGNAL_SOURCE_NUMBER"'", "recipients": ["'"$SIGNAL_TARGET_NUMBER"'"]}' \
  'https://signal.home/v2/send'
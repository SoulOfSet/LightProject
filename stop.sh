#!/usr/bin/bash
PORT=$(cat config.yml | grep -m 1 port | sed -e "s/port://" | tr -d '[:space:]')
ADDRESS='http://localhost:'
ADDRESS+=$PORT
ADDRESS+="/status"

echo "Checking address" $ADDRESS
RESPONSE=$(curl --write-out '%{http_code}' --silent --output /dev/null $ADDRESS)

echo "Response: " $RESPONSE

if [ "$RESPONSE" == "200" ]
then
  sudo fuser -k "${PORT}"/tcp
  echo "Process killed"
else
  echo "Process is not active"
fi
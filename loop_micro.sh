#!/usr/bin/env bash
set -e

source ./config.sh

while true; do
  DATA=$(./pull_weather.sh)
  TEMP=$(echo "$DATA" | grep TEMP | cut -d= -f2)
  HUM=$(echo "$DATA" | grep HUM | cut -d= -f2)

  MSG=$(./format_message.sh "$TEMP" "$HUM")
  ./send_telegram.sh "$MSG"

  sleep "${MICRO_INTERVAL}"
done

#!/usr/bin/env bash
set -e

source ./config.sh

TEXT="$1"

curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${TELEGRAM_CHAT_ID}" \
  -d "text=${TEXT}" \
  -d "parse_mode=Markdown" > /dev/null

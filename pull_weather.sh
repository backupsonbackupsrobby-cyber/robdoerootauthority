#!/usr/bin/env bash
set -e

API_URL="https://api.open-meteo.com/v1/forecast?latitude=-33.8688&longitude=151.2093&hourly=temperature_2m,relativehumidity_2m"

DATA=$(curl -s "$API_URL")

TEMP=$(echo "$DATA" | jq '.hourly.temperature_2m[0]')
HUM=$(echo "$DATA" | jq '.hourly.relativehumidity_2m[0]')

echo "TEMP=${TEMP}"
echo "HUM=${HUM}"

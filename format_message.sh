#!/usr/bin/env bash
set -e

source ./config.sh

TEMP="$1"
HUM="$2"

NOW=$(date +"%Y-%m-%d %H:%M:%S")

cat << MSG
Rob Doe | Sydney Weather Swarm
Time: ${NOW}

Temp: ${TEMP}°C
Humidity: ${HUM}%

Signal: 21st century baby. CHEEEHOOO.
MSG

#!/bin/bash

# .env-Datei laden
set -a
source .env
[ -f .env.local ] && source .env.local
set +a

ENTRY_ID="sensor.sonoff_snzb_02d_temperatur"

HA_URL=$(echo "$HA_URL" | tr -d '\r\n')
HA_TOKEN=$(echo "$HA_TOKEN" | tr -d '\r\n')
ENTRY_ID=$(echo "$ENTRY_ID" | tr -d '\r\n')

#echo "HA_URL = '$HA_URL'"
#echo "HA_TOKEN = '$HA_TOKEN'"

curl -H "Authorization: Bearer ${HA_TOKEN}" \
    -H "Content-Type: application/json" \
    "$HA_URL/api/states/$ENTRY_ID"
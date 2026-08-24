#!/bin/zsh

BOT_1="8989887535:AAGX4N1U18w1KrbkMX_cOr0Y90otZvD7qsc"
BOT_2="8276734769:AAGsGvk7eRfkYLS0ZOkgCFvxWgsx-7pq0-M"
BOT_3="8895929865:AAFVSR-ECLVlo63tqTts_0ZbkABJAAzdIWs"

CHAT_ID="@Aiagency101tenet"
LINK="https://asciinema.org/a/GR4My0LlAPzVeWt7"
MESSAGE="🔴 [LIVE SOVEREIGN PROOF] Terminal recording captured and sealed. Witness the raw mechanics here: $LINK"

for token in "$BOT_1" "$BOT_2" "$BOT_3"; do
    curl -s -X POST "https://api.telegram.org/bot${token}/sendMessage" \
      -d "chat_id=${CHAT_ID}" \
      --data-urlencode "text=$MESSAGE" > /dev/null
done

print "Proof broadcasted to the channel across all bots."

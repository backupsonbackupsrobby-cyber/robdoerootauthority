#!/bin/zsh

BOT_1="8989887535:AAGX4N1U18w1KrbkMX_cOr0Y90otZvD7qsc"
BOT_2="8276734769:AAGsGvk7eRfkYLS0ZOkgCFvxWgsx-7pq0-M"
BOT_3="8895929865:AAFVSR-ECLVlo63tqTts_0ZbkABJAAzdIWs"

CHAT_ID="@Aiagency101tenet"
MODEL="llama3.2"

sys_info=$(uname -a; uptime)
prompt="Analyze system state and provide technical diagnostics: $sys_info"

response=$(curl -s http://localhost:11434/api/generate -d "{
  \"model\": \"$MODEL\",
  \"prompt\": \"$prompt\",
  \"stream\": false
}")

ai_output=$(echo "$response" | grep -o '"response":"[^"]*"' | sed 's/"response":"//g' | sed 's/"//g')
message="[$MODEL] ATOM-TRUTH TELEMETRY:\n$ai_output"

for token in "$BOT_1" "$BOT_2" "$BOT_3"; do
    curl -s -X POST "https://api.telegram.org/bot${token}/sendMessage" \
      -d "chat_id=${CHAT_ID}" \
      --data-urlencode "text=$message" > /dev/null
done

print "Telemetry broadcast complete."

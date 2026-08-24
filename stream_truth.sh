cat << 'EOF' > stream_truth.sh
#!/bin/zsh

BOT_1="8989887535:AAGX4N1U18w1KrbkMX_cOr0Y90otZvD7qsc"
BOT_2="8276734769:AAGsGvk7eRfkYLS0ZOkgCFvxWgsx-7pq0-M"
BOT_3="8895929865:AAFVSR-ECLVlo63tqTts_0ZbkABJAAzdIWs"

CHAT_ID="@Aiagency101tenet"
MODEL="hermes3" # Or opencodeai / llama3.2

# Grab the last few recent commands or active session context
live_data=$(fc -ln -10)

# Prompt the local AI to narrate or analyze the live action
prompt="The user is executing live commands on the ATOM-TRUTH node. Analyze this recent activity stream and report the truth: $live_data"

response=$(curl -s http://localhost:11434/api/generate -d "{
  \"model\": \"$MODEL\",
  \"prompt\": \"$prompt\",
  \"stream\": false
}")

ai_output=$(echo "$response" | grep -o '"response":"[^"]*"' | sed 's/"response":"//g' | sed 's/"//g')
message="⚡ [LIVE TRUTH STREAM] ⚡\n$ai_output"

for token in "$BOT_1" "$BOT_2" "$BOT_3"; do
    curl -s -X POST "https://api.telegram.org/bot${token}/sendMessage" \
      -d "chat_id=${CHAT_ID}" \
      --data-urlencode "text=$message" > /dev/null
done
EOF

chmod +x stream_truth.sh

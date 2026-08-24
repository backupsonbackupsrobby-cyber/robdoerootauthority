cat << 'EOF' > ping_bot.sh
#!/bin/sh
TOKEN="8276734769:AAGsGvk7eRfkYLS0ZOkgCFvxWgsx-7pq0-M"
# Replace with your actual Telegram Chat ID if you have it, or query updates first
# To find your chat ID, message your bot on Telegram then run: curl https://api.telegram.org/bot$TOKEN/getUpdates

echo "🤖 [TELEGRAM] Enter your target Chat ID to dispatch the pivot status:"
read -r CHAT_ID

MESSAGE="🚨 ATOM-TRUTH ALERT: Double pivot executed successfully. Perimeter secure and synchronized."

curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
    -d "chat_id=$CHAT_ID" \
    -d "text=$MESSAGE"

echo -pill "\n📡 Status signal dispatched."
EOF

chmod +x ping_bot.sh

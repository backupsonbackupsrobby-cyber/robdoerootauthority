#!/bin/zsh

MODEL="llama3.2"
PROMPT="Analyze current system state and output telemetry summary."

response=$(curl -s http://localhost:11434/api/generate -d "{
  \"model\": \"$MODEL\",
  \"prompt\": \"$PROMPT\",
  \"stream\": false
}")

echo "$response" | grep -o '"response":"[^"]*"' | sed 's/"response":"//g' | sed 's/"//g'

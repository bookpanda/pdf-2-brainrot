#!/bin/bash

if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
  export TF_VAR_sns_topic_endpoint=$SNS_TOPIC_ENDPOINT
  echo "✅ Environment variables loaded successfully."
else
  echo "❌ .env file not found!"
  exit 1
fi

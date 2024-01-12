#!/bin/bash

log_file="./webhook_receiver.log"

echo "Starting webhook receiver..."

while true; do
    # Listen for incoming webhook events on port 8001
    request=$(nc -l -p 8001)

    # Log the received payload to the file
    echo "Received webhook event: $request" >> "$log_file"

    # Trigger the deployment script and log the result
    echo "Running deployment script..." >> "$log_file"
    ./deploy.sh >> "$log_file" 2>&1

    echo "------------  END OF DEPLOYMENT  ------------" >> "$log_file"
done
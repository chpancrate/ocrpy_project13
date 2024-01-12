#!/bin/bash
# script run when webhooks from Docker Hub detected
# get the new application image and update the docker accordingly

echo "Received webhook event."

# Pull the application new version
docker pull "yourDockerHubRepositoryReference":latest

# Restart the Docker containers using the specific image
docker-compose -f compose.yml up -d --no-deps oc_lettings_site
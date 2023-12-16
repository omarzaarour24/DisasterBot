#!/bin/bash

# Run the Docker container
docker-compose up --build -d db

# Wait for 30 seconds
# sleep 5s

run the python script to create the database tables
python createDatabase.py

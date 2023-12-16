#!/bin/bash

#to create backup database
sudo docker exec -u postgres f8b7aeaf167eccb27e568fb0d090004e429fd3c7810a4e2e0b4b82578560e521 sh -c 'pg_dump -U postgres -d resQBot > /tmp/backup.sql'
sudo docker cp f8b7aeaf167eccb27e568fb0d090004e429fd3c7810a4e2e0b4b82578560e521:/tmp/backup.sql src/db/backups/backup.sql
sshpass -p 'root' scp backup.sql ubuntu@3.218.185.199:backup.sql
python cleardb.py
# sleep 100
echo "database upload complete!!"
#!/bin/bash

# Backup database
mysqldump -u myuser -p mydatabase > /path/to/backup.sql

# Restore database
mysql -u myuser -p mydatabase < /path/to/backup.sql

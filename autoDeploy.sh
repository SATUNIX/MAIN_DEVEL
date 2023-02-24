#!/bin/bash

# Copy files to server
rsync -avz --delete /path/to/local/files user@server:/path/to/remote/files

# Restart server
ssh user@server 'sudo systemctl restart myservice'

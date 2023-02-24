#!/bin/bash

# Create directory if it doesn't exist
if [ ! -d "/path/to/directory" ]; then
    mkdir /path/to/directory
fi

# Copy files to directory
cp /path/to/source/files/* /path/to/directory/

# Delete files older than 7 days
find /path/to/directory -type f -mtime +7 -delete

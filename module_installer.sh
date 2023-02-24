#!/bin/bash

# Check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "pip not found. Installing pip..."
    # Install pip
    sudo apt-get update && sudo apt-get install python3-pip -y
fi

# Install required Python modules from requirements.txt
echo "Installing Python modules from requirements.txt..."
sudo pip3 install -r requirements.txt

echo "Installation complete."

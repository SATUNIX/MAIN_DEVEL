#!/bin/bash

# Update package repositories
sudo pacman -Syy

# Upgrade all packages
sudo pacman -Syu

# Clear pacman cache
sudo pacman -Scc

# Display kernel version
uname -r

# Display pacman version
pacman -V | head -n 1

# Display archlinux keyring version
pacman -Qi archlinux-keyring | grep Version

# Ask user if they want to restart the computer
read -p "Restart computer? [y/n] " choice

if [[ "$choice" =~ ^[Yy]$ ]]; then
    # Restart the computer
    sudo reboot
else
    echo "Please restart the computer manually when convenient."
fi

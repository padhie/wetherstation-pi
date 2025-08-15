#!/bin/bash

# Download the font files (example using curl)
mkdir -p ~/Downloads/comic_neue
cd ~/Downloads/comic_new
curl -LO "https://github.com/googlefonts/comic-neue/releases/download/v1.002/ComicNeue-1.002.zip"
unzip ComicNeue-1.002.zip
cd ComicNeue-1.002

# Install for the current user (create .fonts if it doesn't exist)
mkdir -p ~/.fonts
cp *.ttf ~/.fonts/

# Update font cache
sudo fc-cache -fv
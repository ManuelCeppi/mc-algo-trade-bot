#!/bin/sh

echo "Installing lambda requirements"

cd app
cd src

pip3 install -r requirements.txt

echo "Requirements installed"

echo "Running web server"

python3 -m http.server
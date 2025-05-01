#!/bin/bash

# Create static directory if it doesn't exist
mkdir -p static/fonts

# Download Vazirmatn fonts
echo "Downloading Vazirmatn font files..."
curl -L "https://github.com/rastikerdar/vazirmatn/releases/download/v33.003/Vazirmatn-Regular.woff2" -o static/fonts/Vazirmatn-Regular.woff2
curl -L "https://github.com/rastikerdar/vazirmatn/releases/download/v33.003/Vazirmatn-Bold.woff2" -o static/fonts/Vazirmatn-Bold.woff2

echo "Font files downloaded to static/fonts directory."
echo "Now run 'python manage.py collectstatic' to collect all static files."
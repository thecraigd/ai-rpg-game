#!/bin/bash

# Create a temporary virtual environment
python -m venv temp_env
source temp_env/bin/activate

# Install packages
pip install -r requirements.txt

# Analyze package sizes
echo "Package sizes:"
pip list | tail -n +3 | while read -r package version; do
    size=$(du -sh "$PWD/temp_env/lib/python3.9/site-packages/$package" 2>/dev/null | cut -f1)
    if [ ! -z "$size" ]; then
        echo "$package: $size"
    fi
done

# Deactivate and cleanup
deactivate
rm -rf temp_env
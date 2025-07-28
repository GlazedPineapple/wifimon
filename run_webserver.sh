#!/bin/bash

# The absolute path to the project directory
APP_DIR="/home/aokovacs/Documents/wifimon"

# Activate the virtual environment
source "$APP_DIR/.venv/bin/activate"

# Run the python script
# The 'exec' command replaces the shell process with the python process
python3 "$APP_DIR/webserver.py"

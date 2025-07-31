#!/usr/bin/sudo bash

# The absolute path to the project directory
APP_DIR="/home/aokovacs/Documents/wifimon/eaphammer"

# Activate the virtual environment
source "$APP_DIR/.venv/bin/activate"

# Run the python script
# The 'exec' command replaces the shell process with the python process
python3 "$APP_DIR/eaphammer" --bssid 1C:7E:E5:97:79:B1 --essid Example --channel 2 --interface wlan1 --auth wpa-eap --creds
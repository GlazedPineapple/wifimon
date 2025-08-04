#!/usr/bin/sudo bash

# The absolute path to the project directory
SCRIPT_DIR="$(dirname "$(readlink -f $0)")"

#echo "Script path = $SCRIPT_DIR"

EAP_DIR="$SCRIPT_DIR/eaphammer"

# Activate the virtual environment
source "$EAP_DIR/.venv/bin/activate"

# Run the python script
# The 'exec' command replaces the shell process with the python process
#python3 "$EAP_DIR/eaphammer" --bssid $3 --essid $2 --channel 2 --interface $1 --auth wpa-eap --creds
set -e
python3 "$EAP_DIR/eaphammer" --essid $2 --channel 2 --interface $1 --auth wpa-eap --creds

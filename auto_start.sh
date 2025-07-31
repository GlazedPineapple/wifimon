#!/bin/bash

# --- Configuration ---
PROJECT_DIR="/home/aokovacs/Documents/wifimon"
SERVICE_NAME="wifimon_webserver.service"
UNIT_FILE="/etc/systemd/system/$SERVICE_NAME"
WRAPPER_SCRIPT_SOURCE="$PROJECT_DIR/src/run_webserver.sh"
WRAPPER_SCRIPT_DEST="/usr/local/bin/run_webserver.sh"

# --- Script Logic ---

# 1. Check for root privileges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root (use sudo)"
   exit 1
fi

# 2. Check if the service file already exists
# if [ -f "$UNIT_FILE" ]; then
#     echo "Service '$SERVICE_NAME' already exists. Exiting."
#     exit 0
# fi

echo "Setting up the webserver service..."

# 3. Copy the wrapper script to a system location and make it executable
echo "-> Installing wrapper script to $WRAPPER_SCRIPT_DEST"
cp "$WRAPPER_SCRIPT_SOURCE" "$WRAPPER_SCRIPT_DEST"
chmod +x "$WRAPPER_SCRIPT_DEST"

# 4. Create the systemd unit file
echo "-> Creating systemd unit file at $UNIT_FILE"
cat > "$UNIT_FILE" << EOF
[Unit]
Description=Starts Wifimon web server
After=network.target

[Service]

Type=simple
ExecStart=$WRAPPER_SCRIPT_DEST
WorkingDirectory=$PROJECT_DIR
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF


# 5. Reload systemd, enable and start the new service
echo "-> Reloading systemd and enabling service..."
systemctl daemon-reload
systemctl enable --now "$SERVICE_NAME"

echo "Service '$SERVICE_NAME' was created and started successfully!"

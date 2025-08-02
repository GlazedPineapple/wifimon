#!/bin/bash

# --- Configuration for webserver---
WM_WEB_DIR="/home/aokovacs/Documents/wifimon"
WM_WEB_SERVICE_NAME="wifimon_webserver.service"
WM_WEB_UNIT_FILE="/etc/systemd/system/$WM_WEB_SERVICE_NAME"
WM_WEB_WRAPPER_SCRIPT_SOURCE="$WM_WEB_DIR/run_webserver.sh"
WM_WEB_WRAPPER_SCRIPT_DEST="/usr/local/bin/run_webserver.sh"

# --- Configuration for eaphammer ---
WM_EAP_DIR="/home/aokovacs/Documents/wifimon/eaphammer"
WM_EAP_SERVICE_NAME="wifimon_webserver.service"
WM_EAP_UNIT_FILE="/etc/systemd/system/$WM_WEB_SERVICE_NAME"
WM_EAP_WRAPPER_SCRIPT_SOURCE="$WM_WEB_DIR/run_wifimon_eap.sh"
WM_EAP_WRAPPER_SCRIPT_DEST="/usr/local/bin/run_webserver.sh"

# --- Script Logic ---

# 1. Check for root privileges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root (use sudo)"
   exit 1
fi

# 2. Check if the service file already exists
# if [ -f "$WM_WEB_UNIT_FILE" ]; then
#     echo "Service '$WM_WEB_SERVICE_NAME' already exists. Exiting."
#     exit 0
# fi

echo "Setting up the webserver service..."

# 3. Copy the wrapper script to a system location and make it executable
echo "-> Installing wrapper script to $WM_WEB_WRAPPER_SCRIPT_DEST"
cp "$WM_WEB_WRAPPER_SCRIPT_SOURCE" "$WM_WEB_WRAPPER_SCRIPT_DEST"
chmod +x "$WM_WEB_WRAPPER_SCRIPT_DEST"

# 4. Create the systemd unit file
echo "-> Creating systemd unit file at $WM_WEB_UNIT_FILE"
cat > "$WM_WEB_UNIT_FILE" << EOF
[Unit]
Description=Starts Wifimon web server
After=network.target

[Service]

Type=simple
ExecStart=$WM_WEB_WRAPPER_SCRIPT_DEST
WorkingDirectory=$WM_WEB_DIR
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF


# 5. Reload systemd, enable and start the new service
echo "-> Reloading systemd and enabling service..."
systemctl daemon-reload
systemctl enable --now "$WM_WEB_SERVICE_NAME"

echo "Service '$WM_WEB_SERVICE_NAME' was created and started successfully!"

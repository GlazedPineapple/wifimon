#!/bin/bash

# This script launches Chromium in kiosk mode.
# If 'chromium-browser' is not the correct command on your system,
# you may need to change it to 'chromium'.

exec chromium-browser --start-fullscreen --app=http://172.1.2.3:5000 --disable-infobars --noerrdialogs 
s
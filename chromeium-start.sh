#!/bin/bash

# This script launches Chromium in kiosk mode.
# If 'chromium-browser' is not the correct command on your system,
# you may need to change it to 'chromium'.

exec chromium-browser --app=http://127.1.2.3:5000 --noerrdialogs 
s
#!/bin/env ./.venv/bin/python3

import sys
import subprocess
from subprocess import CalledProcessError


def set_interface_state(iface: str, enabled: bool):
    """Brings the interface up or down."""
    state = 'up' if enabled else 'down'
    print(f"Setting interface {iface} to {state}...")
    subprocess.run(["ifconfig", iface, state], check=True)


def show_interface_status(iface: str):
    """Runs 'iwconfig <interface>' and prints the result."""
    print(f"\n--- Current Status for {iface} ---")
    try:
        # text=True decodes the output as text automatically
        result = subprocess.run(
            ["iwconfig", iface],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Could not get status for {iface}: {e.stderr}")


def set_monitor_mode(iface: str, enabled: bool):
    """Enables or disables monitor mode."""
    # Bring the interface down before changing mode
    try:
        set_interface_state(iface, False)
        if enabled:
            print(f"Enabling monitor mode on {iface}...")
            subprocess.run(["iwconfig", iface, "mode", "monitor"], check=True)
        else:
            print(f"Disabling monitor mode (Managed) on {iface}...")
            subprocess.run(["iwconfig", iface, "mode", "managed"], check=True)

        # Bring the interface back up after changing mode
        set_interface_state(iface, True)
        print(f"Successfully changed mode for {iface}.")

        # Show the final status of the interface
        show_interface_status(iface)
    except CalledProcessError as cpe:
        print(f"----Couldn't change mode of interface '{iface}'----")
        print(cpe)
        return False

    return True


if __name__ == "__main__":
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: sudo ./monitor_mode.py <interface> <mode>")
        print("Example: sudo ./monitor_mode.py wlan0 1")
        print("  <mode>: 1 for monitor mode, 0 for managed mode")
        sys.exit(1)

    interface_name = sys.argv[1]
    try:
        mode_selection = int(sys.argv[2])
        set_monitor_mode(interface_name, mode_selection == 'up')
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running a command: {e}")
        print("Please ensure you are running the script with sudo and the interface name is correct.")
    except ValueError:
        print(f"Error: Invalid mode '{sys.argv[2]}'. Must be a number (1 or 0).")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

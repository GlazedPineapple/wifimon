#!/bin/env ./.venv/bin/python3

import sys
import subprocess

def set_interface_state(iface: str, state: str):
    """Brings the interface up or down."""
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


def set_monitor_mode(iface: str, mode: int):
    """Enables or disables monitor mode."""
    # Bring the interface down before changing mode
    set_interface_state(iface, "down")

    if mode == 1:
        print(f"Enabling monitor mode on {iface}...")
        subprocess.run(["iwconfig", iface, "mode", "monitor"], check=True)
    elif mode == 0:
        print(f"Disabling monitor mode (Managed) on {iface}...")
        subprocess.run(["iwconfig", iface, "mode", "managed"], check=True)
    else:
        print(f"Error: Invalid mode '{mode}'. Use 1 for ON or 0 for OFF.")
        # Bring the interface back up before exiting on error
        set_interface_state(iface, "up")
        return

    # Bring the interface back up after changing mode
    set_interface_state(iface, "up")
    print(f"Successfully changed mode for {iface}.")

    # Show the final status of the interface
    show_interface_status(iface)


if __name__ == "__main__":
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: sudo ./monitorMode.py <interface> <mode>")
        print("Example: sudo ./monitorMode.py wlan0 1")
        print("  <mode>: 1 for monitor mode, 0 for managed mode")
        sys.exit(1)

    interface_name = sys.argv[1]
    try:
        mode_selection = int(sys.argv[2])
        set_monitor_mode(interface_name, mode_selection)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running a command: {e}")
        print("Please ensure you are running the script with sudo and the interface name is correct.")
    except ValueError:
        print(f"Error: Invalid mode '{sys.argv[2]}'. Must be a number (1 or 0).")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
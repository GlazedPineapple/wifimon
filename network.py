#!/bin/env ./.venv/bin/python3

import sdbus
from sdbus_block.networkmanager import NetworkManager, NetworkDeviceGeneric, NetworkDeviceWireless
from sdbus_block.networkmanager.enums import DeviceType

def getInterfaces():
    NetworkManager()
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    network_manager = NetworkManager()
    
    interface_path = network_manager.get_device_by_ip_iface("wlan0")
    interface = NetworkDeviceGeneric(interface_path)

    print(interface.device_type)
    print(DeviceType)

    exit(0)

getInterfaces()
# print(network_manager.devices)

# all_devices = {path: NetworkDeviceGeneric(path) for path in network_manager.devices}

# print()
# print(all_devices)

# # all_devices = {}
# # for path in network_manager.devices:
# #     all_devices[path] = NetworkDeviceGeneric(path)


# wifi_devices = [
#     NetworkDeviceWireless(path)
#     for path, device in all_devices.items()
#     if device.device_type == DeviceType.WIFI
# ]

# wifi_devices = []
# for path, device in all_devices.items():
#     if device.device_type == DeviceType.WIFI:
#         wifi_devices.append(NetworkDeviceWireless(path))


# for device in wifi_devices:
#     print(device.device_type)

# print(wifi_devices)
#!/usr/bin/env python3

import time
import vivint
import carrier

# Set up the connection to the cloud session
session = vivint.VivintCloudSession("john.smith@example.com",
                                    "SuperSecretPassword")

# Setup up carrier device
carrier = carrier.CarrierDevice()

# List all panels (sites) that this user account has access to
panels = session.get_panels()

# In this case, get the first thermostat from the first site
thermostat = panels[0].get_devices(device_type_set=[
    vivint.VivintCloudSession.VivintDevice.DEVICE_TYPE_THERMOSTAT
])[0]

# Get the current state and print it out
print(thermostat.current_state())

# Get the carrier state and print it out
print(carrier.carrier_state(None))

# Set a few thermostat things based on carrier state
thermostat.set_operation_mode(carriercstate.get("mode"))
thermostat.set_fan_mode(carriercstate.get("fan_mode"))

temp = carriercstate.get("coolSetpoint")

if carriercstate.get("mode") == "heat":
    temp = carriercstate.get("heatSetpoint")

thermostat.set_temperature(temp)

# Let the change propagate for a bit
time.sleep(2)
for panel in panels:
    # Update every panel. Doing this also updates devices that
    # were spawned from those panels in-place, unless you set
    # devices' receive_updates property is set to False.
    panel.update_devices()

    # Set Carrier state based on vivint thermostat state
    carrier.set_carrier_state(thermostat.current_state())

# This will likely now reflect the current state of the thermostat
print(thermostat.current_state())

#!/usr/bin/env python3

import time
import vivint

# Set up the connection to the cloud session
session = vivint.VivintCloudSession("john.smith@example.com",
                                    "SuperSecretPassword")

# List all panels (sites) that this user account has access to
panels = session.get_panels()

# In this case, get the first thermostat from the first site
thermostat = panels[0].get_devices(device_type_set=[
    vivint.VivintCloudSession.VivintDevice.DEVICE_TYPE_THERMOSTAT
])[0]

state = thermostat.current_state()

# Get the current state and print it out
print(thermostat.current_state())

# Set a few thermostat things.
#thermostat.set_operation_mode("heat")
#thermostat.set_fan_mode("always")
#thermostat.set_temperature(10)

# Let the change propagate for a bit
time.sleep(2)
for panel in panels:
    # Update every panel. Doing this also updates devices that
    # were spawned from those panels in-place, unless you set
    # devices' receive_updates property is set to False.
    panel.update_devices()

    #compare current state to saved state. if values are different than update carrier unit via api call
    cstate = thermostat.current_state()
    if cstate.humidity != state.humidity or cstate.cooling_setpoint != state.cooling_setpoint or cstate.heating_setpoint != state.heating_setpoint:
        panel.set_carrier_state(cstate)
        state = thermostat.current_state()

# This will likely now reflect the current state of the thermostat
print(thermostat.current_state())

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
carrier_state = thermostat.carrier_state(None)
initial_state = True

# Get the current state and print it out
print(state)
print(carrier_state)

# Set a few thermostat things.
#thermostat.set_operation_mode("heat")
#thermostat.set_fan_mode("always")
#thermostat.set_temperature(10)

# Let the change propagate for a bit
time.sleep(2)
for panel in panels:

    #compare current state to saved state. if values are different than update carrier unit via api call
    while True:
        # Update every panel. Doing this also updates devices that
        # were spawned from those panels in-place, unless you set
        # devices' receive_updates property is set to False.
        panel.update_devices()

        #clear states initially
        vivint_state_changed = False
        carrier_state_changed = False


        #set and compare vivint states
        cstate = thermostat.current_state()
        currentheatingpoint = cstate.get("heating_setpoint")
        heatingpoint = state.get("heating_setpoint")

        currentcoolingpoint = cstate.get("cooling_setpoint")
        coolingpoint = state.get("cooling_setpoint")

        #vivint state changed
        if currentcoolingpoint != coolingpoint or currentheatingpoint != heatingpoint:
            vivint_state_changed = True


        #set and compare carrier states
        carriercstate = thermostat.carrier_state(carrier_state)

        currentheatingpoint = carriercstate.get("heating_setpoint")
        heatingpoint = carrier_state.get("heating_setpoint")

        currentcoolingpoint = carriercstate.get("cooling_setpoint")
        coolingpoint = carrier_state.get("cooling_setpoint") 

        #carrier state changed
        if currentcoolingpoint != coolingpoint or currentheatingpoint != heatingpoint:
            carrier_state_changed = True

        if vivint_state_changed == True or carrier_state_changed == True:
            if vivint_state_changed == True:
                print("vivint panel changed, setting carrier state")
                thermostat.set_carrier_state(cstate)
                state = thermostat.current_state()
                carrier_state = thermostat.carrier_state(carrier_state)
            else:
                print("carrier panel changed, setting vivint state")
                #vivint will need to be in celsius format(unfortunately)
                cpoint = ((float(carriercstate.get("cooling_setpoint")) - 32) / 1.8)
                hpoint = ((float(carriercstate.get("heating_setpoint")) - 32) / 1.8)
                thermostat.set_temperature(None, cpoint, hpoint)
                carrier_state = thermostat.carrier_state(carrier_state)
                state = thermostat.current_state()

        #set initial state to use carrier value(whatever it may be)
        if initial_state == True:
            cpoint = ((float(carriercstate.get("cooling_setpoint")) - 32) / 1.8)
            hpoint = ((float(carriercstate.get("heating_setpoint")) - 32) / 1.8)
            thermostat.set_temperature(None, cpoint, hpoint)
            carrier_state = thermostat.carrier_state(carrier_state)
            state = thermostat.current_state()

        initial_state = False

        time.sleep(60)

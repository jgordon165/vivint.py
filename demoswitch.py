import time
import vivint
from credentials import vivint_email, vivint_pwd
from datetime import datetime

# Set up the connection to the cloud session
session = vivint.VivintCloudSession(vivint_email,
                                    vivint_pwd)

# List all panels (sites) that this user account has access to
panels = session.get_panels()


# Sensors and Switches
switch_one_name = "Living Room Main Lights"
switch_two_name = "Dining Room Lights"

switch_one_default_level = 20
switch_two_default_level = 80

motion_duration_in_seconds = 5

sensor_one_name = "Living Room Motion Detector"
sensor_two_name = "Dining Room Motion Detector"

sensor_one_state = datetime.now()
sensor_two_state = datetime.now()

multiswitches = panels[0].get_devices(device_type_set=[
    vivint.VivintCloudSession.VivintDevice.DEVICE_TYPE_LIGHT_MODULE
])

sensors = panels[0].get_devices(device_type_set=[
    vivint.VivintCloudSession.VivintDevice.DEVICE_TYPE_WIRELESS_SENSOR
])

while True:
    for panel in panels:
        # Update every panel. Doing this also updates devices that
        # were spawned from those panels in-place, unless you set
        # devices' receive_updates property is set to False.
        panel.update_devices()

    for multiswitch in multiswitches:
        state = multiswitch.multi_swtich_state()

        if state.get("name") == switch_one_name:
            switch_one_state = state.get("val") 
            print("switch_one_state")
            print(switch_one_state)
            switch_one = multiswitch
        if state.get("name") == switch_two_name:
            switch_two_state = state.get("val")
            switch_two = multiswitch

    
    for sensor in sensors:
        state = sensor.sensor_state()

        if state.get("name") == sensor_one_name:
            print(state.get("activitytime") - sensor_one_state).total_seconds())
            if (state.get("activitytime") - sensor_one_state).total_seconds() < motion_duration_in_seconds:
                sensor_one_state = state.get("activitytime") 
                sensor_one_state_changed = True
            else:
                sensor_one_state_changed = False
        if state.get("name") == sensor_two_name:
            if (state.get("activitytime") - sensor_two_state).total_seconds() < motion_duration_in_seconds:
                sensor_two_state = state.get("activitytime")
                sensor_two_state_changed = True
            else:
                sensor_two_state_changed = False

    if sensor_one_state_changed == True and switch_one_state == 0:
        switch_one.set_switch(switch_one_default_level)
    if sensor_two_state_changed == True and switch_two_state == 0:
        switch_two.set_switch(switch_two_default_level)

    time.sleep(2)

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

motion_duration_in_seconds = 20

sensor_one_inactivity_in_sec = 1200
sensor_two_inactivity_in_sec = 60

sensor_one_name = "Living Room Motion Detector"
sensor_two_name = "Dining Room Motion Detector"

timestamp_conv_factor = 18000

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
            switch_one = multiswitch
        if state.get("name") == switch_two_name:
            switch_two_state = state.get("val")
            switch_two = multiswitch

    #reset time state
    sensor_one_state = datetime.now()
    sensor_two_state = datetime.now()

    for sensor in sensors:
        state = sensor.sensor_state()

        if state.get("name") == sensor_one_name:
            sensor_one_secs = (timestamp_conv_factor - (sensor_one_state - state.get("activitytime")).total_seconds())
            print(sensor_one_secs)
            if sensor_one_secs < motion_duration_in_seconds:
                sensor_one_state = state.get("activitytime") 
                switch_one_turn_on = True
            else:
                switch_one_turn_on = False

            if sensor_one_secs > sensor_one_inactivity_in_sec:
                switch_one_turn_off = True
            else:
                switch_one_turn_off = False
            
            #if motion is detected within motion_duration(typically 5 seconds), turn on light switch to default setting
            if switch_one_turn_on == True and switch_one_state == 0:
                switch_one.set_switch(switch_one_default_level)

            #turn off light switch if sensor has been inactive for inactivity timeout
            elif switch_one_turn_off == True and switch_one_state != 0:
                switch_one.set_switch(0)
        if state.get("name") == sensor_two_name:
            sensor_two_secs = (timestamp_conv_factor - (sensor_two_state - state.get("activitytime")).total_seconds())
            if sensor_two_secs < motion_duration_in_seconds:
                sensor_two_state = state.get("activitytime")
                switch_two_turn_on = True
            else:
                switch_two_turn_on = False

            if sensor_two_secs > sensor_two_inactivity_in_sec:
                switch_two_turn_off = True
            else:
                switch_two_turn_off = False

            #if motion is detected within motion_duration(typically 5 seconds), turn on light switch to default setting
            if switch_two_turn_on == True and switch_two_state == 0:
                switch_two.set_switch(switch_two_default_level)

            #turn off light switch if sensor has been inactive for inactivity timeout
            elif switch_two_turn_off == True and switch_two_state != 0:
                switch_two.set_switch(0)

    time.sleep(10)



import time
import vivint
from credentials import vivint_email, vivint_pwd

# Set up the connection to the cloud session
session = vivint.VivintCloudSession(vivint_email,
                                    vivint_pwd)

# List all panels (sites) that this user account has access to
panels = session.get_panels()

multiswitches = panels[0].get_devices(device_type_set=[
    vivint.VivintCloudSession.VivintDevice.DEVICE_TYPE_LIGHT_MODULE
])
for multiswitch in multiswitches:
    print(
        "Getting state of multiswitch %d on panel %d" %
        (multiswitch.id(), panels[0].id()))
    state = multiswitch.multi_swtich_state()

    # Now bolt the other context to the state, and write it out.
    print("set arbitrary value to test light on these switches")
    print(state)
    multiswitch.set_switch(60)
    multiswitch.set_switch(20)
    multiswitch.set_switch(40)
    multiswitch.set_switch(0)
#!/usr/bin/env python

import outletswitch

switch = outletswitch.OutletSwitch()

while 1:
    command = raw_input('enter number for command: ')

    print("sending command {}".format(command))
    try:
        if int(command) == 0:
            switch.set_status(False)
        elif int(command) == 1:
            switch.set_status(True)
        elif int(command) == 2:
            print(switch.get_status())
    except Exception as e:
        print(e)

#!/usr/bin/env python

import outletswitch

def measure_response_time(switch):
    # Send the message.
    switch.radio.stopListening()
    switch.radio.write(bytes(1))
    switch.radio.startListening()

    # Wait here until for a response, or timeout.
    started_waiting_at = switch.millis()
    while not switch.radio.available():
        if (switch.millis() - started_waiting_at) > 1000:
            raise Exception('response timed out')

    print('Response took {0} ms'.format(switch.millis() - started_waiting_at))

    return switch.radio.read(switch.radio.getDynamicPayloadSize())


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
        elif int(command) == 3:
            print(measure_response_time(switch))
    except Exception as e:
        print(e)

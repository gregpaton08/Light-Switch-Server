#!/usr/bin/env python

import outletswitch
import sys

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


def run_test_mode(switch):
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


def set_switch_status(switch, status):
    retries = 5
    while retries:
        try:
            switch.set_status(status)
            return
        except Exception as e:
            retries -= 1
    print('ERROR: failed to set switch status')


switch = outletswitch.OutletSwitch()

if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg.lower() == 'true' or arg.lower() == 'on' or arg == '1':
        set_switch_status(switch, True)
    elif arg.lower() == 'false' or arg.lower() == 'off' or arg == '0':
        set_switch_status(switch, False)
    else:
        print('ERROR: invalid command {0}'.format(arg))
else:
    run_test_mode(switch)
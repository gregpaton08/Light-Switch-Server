#!/usr/bin/env python

from switch_hardware import server
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {0} <state = on, off>'.format(sys.argv[0]))
        quit()

    switch = server.outletswitch.OutletSwitch()

    state = sys.argv[1].lower()
    if state == 'on':
        switch.set_status(True)
    elif state == 'off':
        switch.set_status(False)
    else:
        print('Invalid state {0}'.format(state))



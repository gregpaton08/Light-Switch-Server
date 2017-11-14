#!/usr/bin/env python

import time
from RF24 import *

### NRF24l01 pinout
# 1 GND  =>  ground
# 2 VCC  =>  3.3V
# 3 CE   =>  GPIO22
# 4 CSN  =>  SPI CE0
# 5 SCK  =>  CPI CLK
# 6 MOSI =>  SPI MOSI
# 7 MISO =>  SPI MISO
# 8 IRQ  =>  ?
radio = RF24(22, 0);


reading_pipe = 0xF0F0F0F0E1
writing_pipe = 0xF0F0F0F0D2
millis = lambda: int(round(time.time() * 1000))


def setup():
    radio.begin()
    radio.enableDynamicPayloads()
    radio.setRetries(5, 15)
    # radio.printDetails()

    radio.openReadingPipe(1, reading_pipe)
    radio.openWritingPipe(writing_pipe)
    radio.startListening()


def send_data(data):
    # First, stop listening so we can talk.
    radio.stopListening()

    # Take the time, and send it.  This will block until complete
    print('Now sending length {} ... '.format(data))
    radio.write(bytes(data))

    # Now, continue listening
    radio.startListening()

    # Wait here until we get a response, or timeout
    started_waiting_at = millis()
    timeout = False
    while (not radio.available()) and (not timeout):
        if (millis() - started_waiting_at) > 1000:
            timeout = True

    # Describe the results
    if timeout:
        print('failed, response timed out.')
    else:
        # Grab the response, compare, and send to debugging spew
        len = radio.getDynamicPayloadSize()
        receive_payload = radio.read(len)

        # Spew it
        print('got response size={} value="{}"'.format(len, receive_payload.decode('utf-8')))


def get_switch_status():
    """
    Get the current status of the switch.

    :returns: True if the switch is on and False if the switch is off.
    :raises TimeoutError: Raises exception if the request times out.
    """

    radio.stopListening()
    radio.write(bytes(2))
    radio.startListening()

    # Wait here until we get a response, or timeout.
    started_waiting_at = millis()
    timeout = False
    while (not radio.available()) and (not timeout):
        if (millis() - started_waiting_at) > 500:
            timeout = True

    # Describe the results
    if timeout:
        raise Exception('Status request timed out')
    else:
        # Grab the response, compare, and send to debugging spew
        len = radio.getDynamicPayloadSize()
        receive_payload = radio.read(len)

        if receive_payload == "1":
            return True
        return False


setup()

while 1:
    command = input('enter number for command: ')

    print("sending command {}".format(command))
    if int(command) == 2:
        try:
            print(get_switch_status())
        except:
            print('request timed out')
    else:
        send_data(int(command))

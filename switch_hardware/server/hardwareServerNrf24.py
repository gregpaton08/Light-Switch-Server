#!/usr/bin/env python

import time
from RF24 import *
import RPi.GPIO as GPIO

irq_gpio_pin = None

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

# Setup for connected IRQ pin, GPIO 24 on RPi B+; uncomment to activate
#irq_gpio_pin = RPI_BPLUS_GPIO_J8_18
#irq_gpio_pin = 24

##########################################
def try_read_data(channel=0):
    if radio.available():
        while radio.available():
            len = radio.getDynamicPayloadSize()
            receive_payload = radio.read(len)
            print('Got payload size={} value="{}"'.format(len, receive_payload.decode('utf-8')))
            # First, stop listening so we can talk
            radio.stopListening()

            # Send the final one back.
            radio.write(receive_payload)
            print('Sent response.')

            # Now, resume listening so we catch the next packets.
            radio.startListening()

reading_pipe = 0xF0F0F0F0E1
writing_pipe = 0xF0F0F0F0D2
min_payload_size = 4
max_payload_size = 32
payload_size_increments_by = 4
next_payload_size = 32
inp_role = 'none'
send_payload = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ789012'
millis = lambda: int(round(time.time() * 1000))

print('pyRF24/examples/pingpair_dyn/')
radio.begin()
radio.enableDynamicPayloads()
radio.setRetries(5,15)
radio.printDetails()

print(' ************ Role Setup *********** ')

print('Role: Pong Back, awaiting transmission')
if irq_gpio_pin is not None:
    # set up callback for irq pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(irq_gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(irq_gpio_pin, GPIO.FALLING, callback=try_read_data)

radio.openReadingPipe(1, reading_pipe)
radio.openWritingPipe(writing_pipe)
radio.startListening()

# forever loop
while 1:
    # Pong back role.  Receive each packet, dump it out, and send it back

    # if there is data ready
    if irq_gpio_pin is None:
        # no irq pin is set up -> poll it
        try_read_data()
    else:
        # callback routine set for irq pin takes care for reading -
        # do nothing, just sleeps in order not to burn cpu by looping
        time.sleep(1000)

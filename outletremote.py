import RPi.GPIO as GPIO
import time

class OutletRemote:
    def __init__(self):
        self.gpio_pin_on = 25
        self.gpio_pin_off = 24

        GPIO.setmode(GPIO.BCM)

        GPIO.setup([self.gpio_pin_on, self.gpio_pin_off], GPIO.OUT, initial=GPIO.LOW)

    def __toggle_gpio_channel(self, channel, seconds=5.0):
        GPIO.output(channel, GPIO.HIGH)
        if seconds > 0:
            time.sleep(seconds)
        GPIO.output(channel, GPIO.LOW)

    def set(self, on):
        channel = self.gpio_pin_on if on else self.gpio_pin_off
        self.__toggle_gpio_channel(channel)


if __name__ == '__main__':
    switch = OutletRemote()
    switch.set(False)
    time.sleep(2)
    switch.set(True)

    # GPIO.cleanup()
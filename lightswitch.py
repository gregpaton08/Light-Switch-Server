try:
    import RPi.GPIO as GPIO
except ImportError:
    from gpiostubs import GPIO

import time

class LightSwitch:
    def __init__(self):
        self.gpio_pin_on = 25
        self.gpio_pin_off = 24

        GPIO.setmode(GPIO.BCM)

        GPIO.setup([self.gpio_pin_on, self.gpio_pin_off], GPIO.OUT, initial=GPIO.LOW)

    def __toggle_gpio_channel(self, channel, seconds = 0.5):
        GPIO.output(channel, GPIO.HIGH)
        time.sleep(seconds)
        GPIO.output(channel, GPIO.LOW)

    def set_light(self, on):
        channel = self.gpio_pin_on if on else self.gpio_pin_off
        self.__toggle_gpio_channel(channel)

    def cleanup(self):
        GPIO.cleanup()


if __name__ == '__main__':
    light = LightSwitch()
    light.set_light(False)
    time.sleep(2)
    light.set_light(True)

    GPIO.cleanup()
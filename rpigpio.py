import RPi.GPIO as GPIO
import time

if __name__ == "__main__":
        channel = 17
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(channel, GPIO.OUT)
	GPIO.output(channel, GPIO.HIGH)
	time.sleep(5)
	GPIO.output(channel, GPIO.LOW)
	GPIO.cleanup()

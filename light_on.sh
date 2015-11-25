python - <<END
import RPi.GPIO as GPIO
import time
channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)
GPIO.output(channel, GPIO.HIGH)
time.sleep(2)
GPIO.output(channel, GPIO.LOW)
GPIO.cleanup(channel)
exit()
END

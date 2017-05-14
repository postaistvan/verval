from gpiozero import DistanceSensor
import RPi.GPIO as GPIO
import Adafruit_DHT

GPIO.setmode(GPIO.BCM)
import time

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 22)
print humidity
print temperature

TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, True)
time.sleep(0.00001)
pulse_start = time.time()
GPIO.output(TRIG, False)

while GPIO.input(ECHO) == 0:
    pulse_start = pulse_start

pulse_end = time.time()

pulse_duration = pulse_end - pulse_start

distance = pulse_duration * 17150

distance = round(distance, 2)

print distance

GPIO.cleanup()

# First test code for NEMA23 motor with TB6600 - DPM 2021.03.29
# Connected to 4 of 6 wires for twin-coil stepper motor
# Using common anode configuration with GND tied to ENA(-), PUL(-), and DIR(-)
# Connect GPIO pins as shown below) to the "+" input for each: ENA, PUL, and DIR

import time
import RPi.GPIO as GPIO

PUL = 13 # Stepper Drive Pulses
DIR = 19 # Controller Direction Bit (High for Controller default / LOW to Force a Directi$
ENA = 26 # Controller Enable Bit (High to Enable / LOW to Disable).
# Note: Leave DIR and ENA disconnected, and the controller WILL drive the motor in Defaul$

GPIO.setmode(GPIO.BCM) # BCM pin numbers (as opposed to board pin numbers)
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

print('PUL = GPIO 13')
print('DIR = GPIO 19')
print('ENA = GPIO 26')
print('Initialization Completed')

durationFwd = 3000                             # This is the duration of the motor spinni$
durationBwd = 3000                             # This is the duration of the motor spinni$
print('Duration Fwd set to ' + str(durationFwd))
print('Duration Bwd set to ' + str(durationBwd))
delay = 0.00025                                   # The delay between PUL pulses - effect$
print('Speed set to ' + str(delay))

cycles = 5 # This is the number of cycles to be run once program is started.
cyclecount = 0 # This is the iteration of cycles to be run once program is started.
print('number of Cycles to Run set to ' + str(cycles))


def forward():
    GPIO.output(ENA, GPIO.LOW)         # dpm inverted
    print('ENA set to HIGH - Controller Enabled')
    time.sleep(.5)                      # pause due to a possible change direction
    GPIO.output(DIR, GPIO.LOW)          # forward direction
    print('DIR set to LOW - Moving Forward at ' + str(delay))
    print('Controller PUL being driven.')
    for x in range(durationFwd):
        GPIO.output(PUL, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        time.sleep(delay)
    GPIO.output(ENA, GPIO.HIGH)          # dpm inverted
    print('ENA set to LOW - Controller Disabled')
    time.sleep(.5)                      # pause for possible change direction
    return

  def reverse():
    GPIO.output(ENA, GPIO.LOW)
    print('ENA set to HIGH - Controller Enabled')
    time.sleep(.5)                      # pause due to a possible change direction
    GPIO.output(DIR, GPIO.HIGH)         # reverse direction
    print('DIR set to HIGH - Moving Backward at ' + str(delay))

    while cyclecount < cycles:
    forward()
    reverse()
    cyclecount = (cyclecount + 1)
    print('Number of cycles completed: ' + str(cyclecount))
    print('Number of cycles remaining: ' + str(cycles - cyclecount))

GPIO.cleanup()
print('Cycling Completed')

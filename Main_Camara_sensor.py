# Programa para la raspberry pi
# Captura de imagenes activadas por un sensor
# Creado por: Juan Felipe Monsalvo

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT LIBRARIES
# ----------------------------------------------------------------------------------------------------------------------
import cv2
import time
import numpy as np

import picamera
import RPi.GPIO as GPIO
from gpiozero import Button

# ----------------------------------------------------------------------------------------------------------------------
# SETTING THE GPIO BOARD
# ----------------------------------------------------------------------------------------------------------------------
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)

# set GPIO Pins
TRIG = 7
ECHO = 12

# set GPIO direction (IN / OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.output(TRIG, False)

GPIO.setup(ECHO, GPIO.IN)

# Button Definition
button = Button(26)    # Button pin definition
# ----------------------------------------------------------------------------------------------------------------------
# FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------
def distance():
    # set Trigger to HIGH
    GPIO.output(TRIG, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # save StartTime
    while GPIO.input(ECHO) == 0:
        pass
    StartTime = time.time()

    # save time of arrival
    while GPIO.input(ECHO) == 1:
        pass
    StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance_cm = (TimeElapsed * 34300) / 2

    return distance_cm


# ----------------------------------------------------------------------------------------------------------------------
# MAIN CODE
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        while True:
            # Waiting for the button activation in order to continue with the program
            button.wait_for_press()

            # Definition of t_end = 10 seconds. The maximum period of time where the camera program is active
            t_end = time.time() + 10

            dist = distance()
            print("Measured Distance = %.1f cm" % dist)
            time.sleep(1)

            # Escape key in order to close the process and return to stand by position
            if cv2.waitKey(20) == 27 or time.time() > t_end or button.is_pressed:
                break

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()


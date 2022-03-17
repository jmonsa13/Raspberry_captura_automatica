# Programa para la raspberry pi
# Captura de imagenes activadas por un sensor
# Creado por: Juan Felipe Monsalvo

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT LIBRARIES
# ----------------------------------------------------------------------------------------------------------------------
import cv2
import time
import numpy as np
import sys

import RPi.GPIO as GPIO
from gpiozero import Button

# ----------------------------------------------------------------------------------------------------------------------
# SETTING THE GPIO BOARD
# ----------------------------------------------------------------------------------------------------------------------
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
TRIG = 4  # Physical pin # 7
ECHO = 18 # Physicial pin # 12
button = Button(26)    # Physical pin # 37

# set GPIO direction (IN / OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.output(TRIG, False)

GPIO.setup(ECHO, GPIO.IN)
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


def avg_distance(n=2):
    # Inicializando variable
    avg_dist = 0
    
    # Cuantas mediciones se toman
    for i in range(n):
        # Measuring distance
        avg_dist += distance()
        
        # Waiting time between measure
        time.sleep(1)
    
    return avg_dist/n


# ----------------------------------------------------------------------------------------------------------------------
# MAIN CODE
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # Starting message
    print("Inicializando")
    time.sleep(1)

    # Initialization
    count = 0
            
    #Definition of t_end = 60 seconds. The maximum period of time where the camera program is active
    t_end = time.time() + 86400 * 5
            
    while True:
        try:
            # Taking the distance            
            avg_dist = avg_distance(n=5)
            
            print("Measured Distance = %.1f cm" % avg_dist)

            # Taking the picture
            if avg_dist <= 250:             
                
                # Wait final position of the transfer
                time.sleep(2)
                
                # Take n photos in intervals of 5 seconds each
                for num in range(1):
                
                    # Camera turn on
                    cap = cv2.VideoCapture(0)
                    
                    # Resolution of the camera ASPECT RATIO 4:3
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # Max 2592 | 1280 | 1920
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440) # Max 1944 | 962 |1440

                    # Do while the video camera is on
                    while cap.isOpened():
                        # Read Video frame by frame
                        ret, frame = cap.read()

                        if ret is False:
                            break
                    
                        # Count
                        count += 1

                        # Saving the image
                        print("Saving the image")
                        img_name = "./Images/Testing_{}.png".format(count)
                        cv2.imwrite(img_name, frame)
                        
                        
                        # When everything done, release the capture
                        cap.release()
                        cv2.destroyAllWindows()
                        
                    # Sleeping for 5 seconds between measure
                    print("Sleeping for 5 seconds")
                    time.sleep(5)
                    
                # Wait for the transfer to move out
                print("Waiting for tranfer to move out for 90 seconds")
                time.sleep(90)
                    
            # Waiting time between measure
            time.sleep(2)         

            # Escape key in order to close the process and return to stand by position
            if cv2.waitKey(20) == 27 or time.time() > t_end:
                print("Measurement stopped by User")
                GPIO.cleanup()
                sys.exit(0)
                 
        # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()


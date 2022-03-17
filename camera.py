from picamera import PiCamera
import time

camera = PiCamera()

print("Starting the camera")
camera.start_preview()
time.sleep(10)

print("Taking the picture")
camera.capture("/home/pi/Desktop/Raspberry_captura_automatica/Test_img.jpg")
camera.stop_preview()
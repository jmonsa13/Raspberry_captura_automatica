from picamera import PiCamera
import time

camera = PiCamera()

camera.start_preview()
time.sleep(10)
camera.capture("/home/pi/Desktop/Raspberry_captura_automatica/Test_img.jpg")
camera.stop_preview()
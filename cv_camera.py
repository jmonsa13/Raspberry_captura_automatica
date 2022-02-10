import cv2
from gpiozero import Button

# Button Definition
button = Button(26)    # Button pin definition

# Waiting for the button activation in order to continue with the program
button.wait_for_press()

# Camera initialization
cap = cv2.VideoCapture(0)

# Do while the video camera is on
while cap.isOpened():
    # Read Video frame by frame
    ret, frame = cap.read()

    if ret is False:
        break
        
    # Showing the image
    cv2.imshow("Video", frame)
    
    # Escape key in order to close the process and return to stand by position
    if cv2.waitKey(20) == 27 or button.is_pressed:
        # Saving the image
        print("Saving the image")
        img_name = "Testing_{}.png".format(1)
        cv2.imwrite(img_name, frame)
        
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
        break

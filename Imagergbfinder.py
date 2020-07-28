import picamera
import matplotlib.image as img
from PIL import Image
import cv2
import numpy as np
import RPi.GPIO as GPIO          
import time
import os
myCmd = 'python3 /home/pi/Imagergbfinder.py'


getrgb= True
track = False

row = 80
column = 35
darkestred = 1000
darkestgreen = 1000
darkestblue = 1000
lightred = 0
lightgreen = 0
lightblue = 0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

TRIG = 3
ECHO = 5
ena=22
enb=32
GPIO.setup(TRIG, GPIO.OUT)


GPIO.setup(ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)      


GPIO.setup(18,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.setup(10, GPIO.IN)
GPIO.setup(38, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(40, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(35, GPIO.OUT, initial=GPIO.HIGH)
GPIO.output(18,False)
GPIO.output(16,False)
GPIO.output(26,False)
GPIO.output(24,False)
GPIO.input(10)
p=GPIO.PWM(ena, 1000)
p2=GPIO.PWM(enb, 1000)
p.start(22)
p2.start(32)

with picamera.PiCamera() as camera:
    camera.resolution = (180, 90)
    camera.capture("/home/pi/Desktop/colors.jpg")
print("Picture Taken")

def stop(os):
    os.system(myCmd)

while getrgb == True:
    GPIO.output(35, GPIO.LOW)
    GPIO.output(40, GPIO.HIGH)
    GPIO.output(38, GPIO.LOW)
    
    colors_image = img.imread('/home/pi/Desktop/colors.jpg')

    img1 = cv2.imread('/home/pi/Desktop/colors.jpg', 1)
    colors_frame = cv2.cvtColor(img1, cv2.COLOR_RGB2HSV)
    filename = '/home/pi/Desktop/hsvphoto.jpg'

    cv2.imwrite(filename, colors_frame)

    image = Image.open('/home/pi/Desktop/hsvphoto.jpg')
    r2, g2, b2 = image.getpixel((row, column))
    
    if (row >= 100):
        column = column +1
        row = 80
    if (column >= 55):
        getrgb = False
        print(lightred)
        print(lightgreen)
        print(lightblue)
        print(darkestred)
        print(darkestgreen)
        print(darkestblue)
        track = True
    row = row +1
    
    
    if (r2 < darkestred): 
        darkestred = r2
    if (g2 < darkestgreen): 
        darkestgreen = g2
    if (b2 < darkestblue):
        darkestblue = b2


    if (r2 > lightred): 
        lightred = r2
    if (g2 > lightgreen): 
        lightgreen = g2
    if (b2 > lightblue):
        lightblue = b2
    if GPIO.input(10) == True:
        GPIO.output(38, False)
        GPIO.output(40, False)
        GPIO.output(35, False)
        stop(os)


darkestred -= 20
darkestblue -= 20
darkestgreen -= 20

lightred += 20
lightblue += 20
lightgreen += 20

print(lightred)
print(lightgreen)
print(lightblue)
print(darkestred)
print(darkestgreen)
print(darkestblue)
GPIO.output(35, GPIO.LOW)
GPIO.output(40, GPIO.LOW)
GPIO.output(38, GPIO.LOW)
    
cap = cv2.VideoCapture(0)
while track == True:

    _, frame = cap.read()
    rows, cols, _=frame.shape
    
    x_medium = int(cols / 2)
    center = int(cols/ 2)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    low_color = np.array([darkestblue, darkestgreen, darkestred])
    High_color = np.array([lightblue, lightgreen, lightred])
    ##low_color = np.array([161, 155, 84])
    ##High_color = np.array([179, 255, 255])
    mask = cv2.inRange(hsv_frame, low_color, High_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    for cnt in contours:
        (x, y, w, h)= cv2.boundingRect(cnt)
        
        #cv2.rectangle(frame, (x, y), (x + w, y+h), (0, 255, 0), 2)
        x_medium = int((x + x + w) / 2)
        break
    
    cv2.line(frame, (x_medium, 0), (x_medium, 480), (255, 0, 0), 2)
    cv2.imshow("", mask)    
    cv2.imshow('RGB', frame)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
    
    if GPIO.input(10) == True:
        break

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    #while GPIO.input(ECHO) == 0:
    start = time.time()
    
    GPIO.wait_for_edge(ECHO, GPIO.FALLING)
    #while GPIO.input(ECHO) ==1:
    stop = time.time()
    #print("recieved")

    print((stop-start) * 17150)
    TimeElapsed = (stop - start) * 17000

    if TimeElapsed >64 and x_medium < center +60 and x_medium > center -60:
        p.ChangeDutyCycle(80)
        p2.ChangeDutyCycle(80)
        GPIO.output(18,False)
        GPIO.output(16,True)
        GPIO.output(26,False)
        GPIO.output(24,True)
        print("Forwards")
        time.sleep(.05)
    if TimeElapsed < 53 and x_medium < center +60 and x_medium > center -60:
        p.ChangeDutyCycle(80)
        p2.ChangeDutyCycle(80)
        GPIO.output(18,True)
        GPIO.output(16,False)
        GPIO.output(26,True)
        GPIO.output(24,False)
        print("Backwards")
        time.sleep(.05)
    print((stop-start) * 17000)
    
    if x_medium == center:
        GPIO.output(35, GPIO.HIGH)
        GPIO.output(40, GPIO.LOW)
        GPIO.output(38, GPIO.HIGH)
    else:
        GPIO.output(35, GPIO.LOW)
        GPIO.output(40, GPIO.LOW)
        GPIO.output(38, GPIO.LOW)
    if x_medium < center - 60:
        p.ChangeDutyCycle(80)
        p2.ChangeDutyCycle(80)
        GPIO.output(18,True)
        GPIO.output(16,False)
        GPIO.output(26,False)
        GPIO.output(24,True)
        print("Right")
        time.sleep(.05)
        GPIO.output(18,False)
        GPIO.output(16,False)
        GPIO.output(26,False)
        GPIO.output(24,False)
    elif x_medium > center + 60:
        p.ChangeDutyCycle(80)
        p2.ChangeDutyCycle(80)
        GPIO.output(18,False)
        GPIO.output(16,True)
        GPIO.output(26,True)
        GPIO.output(24,False)
        print("Left")
        time.sleep(.05)
        GPIO.output(18,False)
        GPIO.output(16,False)
        GPIO.output(26,False)
        GPIO.output(24,False)
    else:
        GPIO.output(18,False)
        GPIO.output(16,False)
        GPIO.output(26,False)
        GPIO.output(24,False)
        print("stop")
    
    '''
    if x_medium < center +70 and x_medium > center -70:
        GPIO.output(18,False)
        GPIO.output(16,False)
        GPIO.output(26,False)
        GPIO.output(24,False)
        print("stop")
    '''
GPIO.output(40, True)
stop(os)
cap.release()
cv2.destroyAllWindows()



     
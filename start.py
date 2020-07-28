import picamera
import os
import time
#from pynput.mouse import Button, Controller
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN)
GPIO.setup(38, GPIO.OUT, initial=GPIO.LOW)
GPIO.input(10)
#mouse = Controller()
myCmd = 'python3 /home/pi/Imagergbfinder.py'
#time.sleep(5)
#mouse.position = (143, 21)
#time.sleep(2)
#mouse.press(Button.left)
#mouse.release(Button.left)
while True:
	GPIO.output(38, GPIO.LOW)
	if GPIO.input(10) == True:
		os.system(myCmd)
		time.sleep(5)



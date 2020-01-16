
from flask import Flask
#from car import *
import time
# import stream_client
import time

import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.output(13,False)
GPIO.output(12,False)
GPIO.output(7,False)
GPIO.output(11,False)
p=GPIO.PWM(13, 50)
#p.start(50)
def pause():
	GPIO.output(13,False)
	p.ChangeDutyCycle(0)
	GPIO.output(12,False)
	GPIO.output(7,False)
	GPIO.output(11,False)

def right():
	start=time.time()*1000
	while time.time()*1000 <= start+5:
		GPIO.output(13,True)
		p.start(40)
		p.ChangeDutyCycle(55)
		GPIO.output(12,False)
	        GPIO.output(7,True)
		GPIO.output(11,False)
	#p.ChangeDutyCycle(55)

def left():
	start=time.time()*1000

	while time.time()*1000 <= start+5:
		GPIO.output(13,True)
		p.start(40)
		p.ChangeDutyCycle(55)
		GPIO.output(12,False)
		GPIO.output(7,False)
		GPIO.output(11,True)
	#p.ChangeDutyCycle(55)

def forward():
	GPIO.output(13,True)
	p.start(40)
	p.ChangeDutyCycle(80)
	GPIO.output(12,False)
	GPIO.output(7,False)
	GPIO.output(11,False)
	p.ChangeDutyCycle(25)
	#start=time.time()y


def stop():
	GPIO.output(13,False)
	#p.start(0)
	p.ChangeDutyCycle(0)
        p.stop()
	GPIO.output(12,False)
	GPIO.output(7,False)
	GPIO.output(11,False)

def rev():
	#GPIO.output(13,False)
	p.ChangeDutyCycle(0)
	GPIO.output(12,True)
	GPIO.output(7,False)
	GPIO.output(11,False)



app = Flask(__name__)          

@app.route('/forward', methods=['GET'])
def fwd():	
    forward()
    print('forward')
    return "Forward"


@app.route('/reverse', methods=['GET'])
def reve():	
    rev()
    print('rev')
    return "Reverse"

@app.route('/left', methods=['GET'])
def left_turn():
    left()
    return "Turn Left"

@app.route('/pause', methods=['GET'])
def pause_mot():
    pause()
    return "break"

@app.route('/right', methods=['GET'])
def right_turn():
    right()
    return "Turn Right"

@app.route('/stop', methods=['GET'])
def end():
    stop()
   # p.stop()
    return "stop"
	
if __name__ == "__main__":
	app.run(debug=True, port=5000, host='0.0.0.0')

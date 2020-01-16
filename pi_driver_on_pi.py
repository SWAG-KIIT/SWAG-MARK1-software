import io
import socket
import struct
import time
import picamera
import cv2
import numpy as np
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
#pwm = GPIO.PWM(13, 25)
GPIO.output(13,False)
GPIO.output(12,False)
GPIO.output(7,False)
GPIO.output(11,False)


print("about to connect")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind(('192.168.43.255',7000))
print("got socket")
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect(('192.168.43.224', 8000))
print("finish connection")
connection = client_socket.makefile('wb')

class NeuralNetwork(object):
    def __init__(self):
        #self.model = cv2.ml.ANN_MLP_create()
        self.model = cv2.ml.ANN_MLP_load('ann.xml')
        #self.layer_sizes = np.int32([50400, 32, 3])
        #self.model.setLaqerSizes(self.layer_sizes)
        #self.model.load('ann_91.xml')

    def predict(self, samples):
        ret, resp = self.model.predict(samples)
        return resp.argmax(-1)

ann = NeuralNetwork()
instruction_bit = 0
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (420,240)
        camera.framerate = 10
        camera.rotation=180
        time.sleep(2)
        start = time.time()
        stream = io.BytesIO()
        instruct = 0
	GPIO.output(7, False)
        GPIO.output(11, False)
        for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
	    streamValue = stream.read()
            connection.write(streamValue)
	    image = cv2.imdecode(np.fromstring(streamValue, dtype=np.uint8), -1)
	    stream.seek(0)
            stream.truncate()
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # gray_image = cv2.flip(gray_image, 1)
            gray_image = gray_image[120:240, :]
            # added6
            gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
            gray_image = cv2.Laplacian(gray_image, cv2.CV_64F)
            gray_image = cv2.erode(gray_image, kernel=(3, 3), iterations=3)
            gray_image = cv2.erode(gray_image, kernel=(4, 4))
            gray_image = cv2.dilate(gray_image, kernel=(2, 2), iterations=2)
            gray_image = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel=(3, 3))
            # done

            temp_image_array = gray_image.reshape(1, 50400).astype(np.float32)

            prediction = ann.predict(temp_image_array)

            #if instruction_bit >=6:
                #GPIO.output(7, False)
                #GPIO.output(11, False)
		#instruction_bit=0

            if prediction == 0:
                #pwm.ChangeDutyCycle(20)
		GPIO.output(13, True)
                GPIO.output(12, False)
                GPIO.output(7, False)
                GPIO.output(11, False)
                print('forward')

            elif prediction == 1:
                #pwm.ChangeDutyCycle(10)
		GPIO.output(13, True)
                GPIO.output(12, False)
                GPIO.output(7, False)
                GPIO.output(11, True)
                print('left')
		time.sleep(0.06)
                instruction_bit += 1

            elif prediction == 2:
		#pwm.ChangeDutyCycle(10)
                GPIO.output(13, True)
                GPIO.output(12, False)
                GPIO.output(7, True)
                GPIO.output(11, False)
                print('right')
		time.sleep(0.06)
                instruction_bit += 1

            #elif prediction == 3:
            #   urllib2.urlopen('http://192.168.43.141:5000/stop').read()
            #    print('pause')
	
	    time.sleep(0.06)
	    GPIO.output(7, False)
            GPIO.output(11, False)
	    GPIO.output(13, False)
	    #pwm.ChangeDutyCycle(0)
	    GPIO.output(12, False)
	    time.sleep(0.16)
	    
            instruction_bit += 1

            # only get the lower half image (cut the row num in half)

    connection.write(struct.pack('<L', 0))
except (socket.error, e):
    print(e)
finally:
    connection.close()
    client_socket.close()
    print('connection closed')
    GPIO.cleanup()


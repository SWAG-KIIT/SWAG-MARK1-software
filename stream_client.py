
import io
import socket
import struct
import time
import picamera

print("about to connect")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind(('10.1.185.46',7000))
print("got socket")
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect(('10.1.187.22', 8000))
print("finish connection")
connection = client_socket.makefile('wb')


try:
    with picamera.PiCamera() as camera:
        camera.resolution = (420,240)
        camera.framerate = 10
        camera.rotation=180
        #time.sleep(2)
        start = time.time()
        stream = io.BytesIO()
        instruct = 0

        for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            stream.seek(0)
            stream.truncate()
    connection.write(struct.pack('<L', 0))
except (socket.error, e):
    print(e)
finally:
    connection.close()
    client_socket.close()
    print('connection closed')


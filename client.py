import socket
import json

HOST = '127.0.0.1'
PORT = 5003
s = socket.socket()
s.connect((HOST, PORT))
try:
    color = raw_input('enter a color [red/green/blue]: ')
    s.send(color.encode())
except KeyboardInterrupt:
    s.close()
    print('bye')
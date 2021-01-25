import socket
from common.networking import send_instruction

if __name__ == '__main__':
    address = '127.0.0.1'
    port = 5000
    data = {'name' : 'Noah Herrin'}
    server = socket.socket()
    server.connect((address, port))
    print(send_instruction(server, data))
    server.close()

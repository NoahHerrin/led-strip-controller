import socket
import json
import argparse
import sys

if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument('-host', help='-host <server address>')
    parser.add_argument('-port', help='-port <server port>')
    args = parser.parse_args()

    address = '127.0.0.1' # default address
    port = 5003 # default port
    if args.host:
        address = args.host
    if args.port:
        port = int(args.port)
    
    server = socket.socket()
    server.connect((address, port))
    while True:
        msg = raw_input("> ")
        server.send(msg)
        data = server.recv(1024)
        if data != None:
            msg = data.decode('ascii')
            print(msg)
        else:
            break
         
    server.close()



    
    
    server_address = None
    server_port = None

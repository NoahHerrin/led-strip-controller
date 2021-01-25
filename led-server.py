"""
File: led-server.py
Purpose:
Author: Noah Herrin
Last Modified: 1/11/2020
"""

import socket
from common.networking import recieve_instruction

def start_server(addr, max_queue_len):
    """creates server socket using the provided address details.

    Parameters
    ----------
    addr: (str, int)
        tuple containing the ip address and port for the new socket.
    max_queue_len: int
        specifies the maximum number of connections for the server socket.
    
    Returns
    -------
    socket
        The server socket.
    
    """

    if socket.has_dualstack_ipv6():
        return socket.create_server(addr, backlog = max_queue_len, family=socket.AF_INET6, dualstack_ipv6=True, reuse_port=True)
    else:
        return socket.create_server(addr, reuse_port=True)

if __name__ == '__main__':
        addr = ("", 5000)
        server = start_server(addr,5)
        client, address = server.accept()
        print(recieve_instruction(client))
        client.close()
        server.close()
        
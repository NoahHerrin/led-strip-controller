"""
File: networking.py
Author: Noah Herrin
Purpose: Stores methods related to sending data between the client and server.
Last-Modified: 1/11/2020
"""

import sys
import socket
import json

msg_delimiter = ":^)"

# --------------------------------------------------- #
# methods for abstracting network transactions
# --------------------------------------------------- #


def send_instruction(connection, payload):
	"""abstracts the process for sending messages to the server.

	Parameters
	----------
	connection: socket
		socket for the messages destination.
	payload: a dictionary storing the message to be sent.
		Must be json serializable.

	Returns
	-------
	Boolean
		True if message was able to be sent to
		destination socket, False otherwise.
    """
    # convert instruction dictionary to json to simplify transport.
	payload_json = json.dumps(payload)
	payload_len = len(payload_json + msg_delimiter)


	# send message length
	connection.send((str(socket.htonl(payload_len)) + msg_delimiter).encode('ascii'))
	# send actual message
	connection.send((payload_json + msg_delimiter).encode('ascii'))
	# success
	return True


def recieve_instruction(connection):
	"""abstracts the process of recieving messages

	Parameters
	----------
	connection: socket
		socket where the incoming instruction will be read from.

	Returns
	-------
	dict or None:
		Returns dictionary containing instructions or
		None if message was unable to be recieved.
	"""
	payload_len = 0
	payload = ""

	# read data from socket into buffer
	buffer = ""
	new_data = None
	tokens = None
	while True:
		new_data = connection.recv(64)
		# check if no new data was recieved
		if not new_data:
			print("breakpoint a")
			break
		buffer += new_data.decode('ascii')

		# check if entire segment of msg has been recieved.
		if msg_delimiter in buffer:
			# parse the message length
			tokens = buffer.split(msg_delimiter)
			msg = tokens[0]
			payload_len = socket.ntohl(int(msg))
			# print(f'Acquired payload_len : {payload_len}')
			
			print(payload_len)
			break
	payload = str(tokens[1])
	print(str(payload))
	return True
 
    

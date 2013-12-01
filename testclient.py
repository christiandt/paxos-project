import socket, json


TCP_IP = '10.0.0.14'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.settimeout(1)

data = None

while 1:

	message = raw_input("Command: ")

	try:
		s.send(message)
	except:
		print "Could not send message, disconnecting"
		s.close()
		break

	if message[0:3] == "END":
		print "goodbye"
		s.close()
		break

	elif message[0:8] == "SHUTDOWN":
		print "Server going down"
		s.close()
		break

	data = ""

	while 1:
		try:
			part = s.recv(BUFFER_SIZE)
			if part[0:8] != "PROPOSE:" and part[0:7] != "ACCEPT:" and part[0:7] != "DECIDE:":
				data += str(part)
		except socket.timeout:
			break
	if data != "":
		print data
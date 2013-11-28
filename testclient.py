import socket


TCP_IP = '10.0.0.14'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))


while 1:
	message = raw_input("Command: ")

	try:
		s.send(message)
		data = s.recv(BUFFER_SIZE)
		print data
		if data[0:7] == "GOODBYE":
			s.close()
			break

	except:
		print "DISCONNECTED"
		s.close()
		break


import cPickle as pickle
import socket, select, sys

BUFFER_SIZE = 1024
connections = []

def getLog():
	try:
		logFile = open("log.p", "rb")
		log = pickle.load(logFile)
		logFile.close
		return log
	except:
		return []

def saveLog(log):
	try:
		logFile = open("log.p", "wb")
		pickle.dump(log, logFile)
		logFile.close
		return True
	except:
		return False

def handleRead():
	logString = ""
	for post in getLog():
		logString += (post+":")
	return logString[0:-1]

def handlePost(data):
	log = getLog()
	log.append(data)
	if saveLog(log):
		return "SUCCESS"
	else:
		return "FAIL"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("10.0.0.14", 5005))
server.listen(5)
connections.append(server)
print "Server started"


while 1:
	# Check if there are any readable sockets
	readable_sockets,writeable_sockets,error_sockets = select.select(connections,[],[])
	for s in readable_sockets:
		# If there is a new connection
		if s == server:
			connection, address = server.accept()
			connections.append(connection)
			print 'Client connected:', address

		# Else if there is received data
		else:
			while 1:
				data = s.recv(BUFFER_SIZE)

				if data[0:4] == "READ":
					result = handleRead()
					s.send(result)

				elif data[0:5] == "POST:":
					result = handlePost(data[5:])
					s.send(result)

				elif data[0:3] == "END":
					s.send('GOODBYE')
					connections.remove(s)
					s.close()
					print 'Removed'
					break

				elif data[0:8] == "SHUTDOWN":
					print 'Shutting Down'
					#server.shutdown(2)
					s.send('GOODBYE')
					server.close()
					print 'Goodbye'
					sys.exit(0)
				else:
					s.send('INVALID')

				break

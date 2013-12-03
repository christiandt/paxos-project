import socket, select, sys, json
import proposer, acceptor


TCP_IP = socket.gethostbyname(socket.gethostname())
TCP_PORT = 5005
BUFFER_SIZE = 1024
debug = True
connections = []
posts = []
paxosRunning = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((TCP_IP, TCP_PORT))
server.listen(5)
connections.append(server)
print "Server started"
print "Address", TCP_IP, ":", TCP_PORT

ips = ["10.185.35.34", "10.147.130.226", "10.178.43.181", "10.202.138.82", "10.252.60.86"]
for ip in ips:
	if ip != TCP_IP:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((ip, TCP_PORT))
			connections.append(s)
		except:
			print "No contact with", ip



def broadcast(message):
	if debug:
		print "Broadcasting: ", message
	for socket in connections:
		if socket != server:
			try :
				socket.send(message)
			except :
				socket.close()
				connections.remove(socket)

def shutdown():
	for socket in connections:
		if socket != server:
			socket.send('GOINGDOWN:'+TCP_IP)
			socket.close()
	server.close()
	print 'Goodbye'
	sys.exit(0)



while 1:
	# Check if there are any readable sockets
	readable_sockets,writeable_sockets,error_sockets = select.select(connections,[],[])

	for s in readable_sockets:
		# If there is a new connection
		if s == server:
			connection, address = server.accept()
			connections.append(connection)
			connection.send("CATCHUP:"+acceptor.receiveRead())
			print 'Client connected:', address

		# Else if there is received data
		else:
			while 1:

				try:
					receivedData = s.recv(BUFFER_SIZE)
				except:
					print "Did not receive data"
					if s in connections:
						s.close()
						connections.remove(s)

				if debug:
					print receivedData

				if "}" in receivedData:

					for data in receivedData.split("}"):
						if data != "":
							data += "}"

							# Else if we have received a propose-message, forward it to an acceptor 
							if data[0:8] == "PROPOSE:":
								result = data[8:]
								proposed = json.loads(result)
								reply = acceptor.receivePropose(proposed)
								s.send("ACK:"+json.dumps(reply))


							# Else if we have received an ACK-message, an acceptor has accepted our proposal,
							# forwards this to the proposer, which in turn broadcasts an accept-message if
							# it has the majority of the acceptors accept its proposal
							elif data[0:4] == "ACK:":
								result = data[4:]
								result = json.loads(result)
								reply = proposer.receivePromise(result)
								if reply == "RESTART":
									# In this case, propose your own value again, before others in queue
									proposemessage = json.dumps(proposer.prepare(proposer.myValue))
									broadcast("PROPOSE:"+proposemessage)
								# When majority is received, check if conflict has occured (previous proposal accepted,
								# but not decided), if so, insert post first in queue.
								elif reply != None:
									if reply['conflict'] != None:
										post = reply['conflict']
										posts.insert(0, post)
										# Conflict occured, add post to begining of posts, continue as normal
									del reply['conflict']
									reply = json.dumps(reply)
									broadcast("ACCEPT:"+reply)


							# Else if we have received an accept-message, forward this to the acceptor
							# which in turn responds an accepted-message if it accepted the value
							elif data[0:7] == "ACCEPT:":
								result = data[7:]
								result = json.loads(result)
								reply = acceptor.receiveAccept(result)
								s.send("ACCEPTED:"+json.dumps(reply))


							# Else if we have received an accepted-message, forward this to the proposer
							# which in turn broadcasts the decided value if all acceprors have accepted 
							# the value
							elif data[0:9] == "ACCEPTED:":
								result = data[9:]
								result = json.loads(result)
								reply = proposer.receiveAccepted(result)
								if reply == "RESTART":
									proposemessage = json.dumps(proposer.prepare(proposer.myValue))
									broadcast("PROPOSE:"+proposemessage)

								# Reply is None until majority is reached, reply is the value as a string
								elif reply != None:
									broadcast("DECIDE:"+json.dumps({'value': reply}))  #reply is a string

									if not posts:
										paxosRunning = False
									else:
										post = posts.pop(0)
										proposemessage = json.dumps(proposer.prepare(post))
										broadcast("PROPOSE:"+proposemessage)



							# Else if we have received a decide-message, a value has been decided, forward
							# to acceptor which stores the value in the log
							elif data[0:7] == "DECIDE:":
								result = data[7:] #result is a string
								post = json.loads(result)['value']
								acceptor.receiveDecide(post)

				else:
					# If we have received a read-message return the log as a string
					if receivedData[0:4] == "READ":
						result = acceptor.receiveRead()
						s.send(result)


					# Else if we have received a end-message, end this connection
					elif receivedData[0:3] == "END":
						s.send('GOODBYE')
						connections.remove(s)
						s.close()
						print 'Removed'
						break


					# Else if we have received a post-message, start paxos
					elif receivedData[0:5] == "POST:":
						result = receivedData[5:]
						if paxosRunning:
							posts.append(result)
						else:
							proposemessage = json.dumps(proposer.prepare(result))
							broadcast("PROPOSE:"+proposemessage)

					# Else if we have received a shutdown-message, end the connection and end the process
					elif receivedData[0:8] == "SHUTDOWN":
						print 'Shutting Down'
						shutdown()


					elif receivedData[0:10] == 'GOINGDOWN:':
						ip = receivedData[10:]
						if s in connections:
							s.close()
							connections.remove(s)
							print ip, "went down"


					elif receivedData[0:8] == 'CATCHUP:':
						log = receivedData[8:]
						acceptor.saveLogString(log)

					# Else return an invalid-message
					elif receivedData != "":
						s.send('INVALID')


					else:
						try:
							s.send('PING')
						except:
							print "Could not send PING"
							if s in connections:
								s.close()
								connections.remove(s)


				break

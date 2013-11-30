import socket, select, sys, json
import proposer, acceptor


TCP_IP = socket.gethostbyname(socket.gethostname())
TCP_PORT = 5005
BUFFER_SIZE = 1024
connections = []
posts = []
paxosRunning = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((TCP_IP, TCP_PORT))
server.listen(5)
connections.append(server)
print "Server started"
print "Address", TCP_IP, ":", TCP_PORT

# add try-except to connects. Need to handle servers that are not turned on
ips = ["10.0.0.14"]
for ip in ips:
	if ip != TCP_IP:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((ip, TCP_PORT))
			connections.append(s)
		except:
			print "No contact with", ip



def broadcast(message):
	print "Broadcasting: ", message
	for socket in connections:
		if socket != server:
			try :
				socket.send(message)
			except :
				socket.close()
				connections.remove(socket)


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

				try:
					data = s.recv(BUFFER_SIZE)
				except:
					print "lost connetion to someone1"
					if s in connections:
						connections.remove(s)
				print data


				# If we have received a read-message return the log as a string
				if data[0:4] == "READ":
					result = acceptor.receiveRead()
					s.send(result)


				# Else if we have received a end-message, end this connection
				elif data[0:3] == "END":
					s.send('GOODBYE')
					connections.remove(s)
					s.close()
					print 'Removed'
					break


				# Else if we have received a post-message, start paxos
				elif data[0:5] == "POST:":
					result = data[5:]
					if paxosRunning:
						posts.append(result)
					else:
						proposemessage = json.dumps(proposer.prepare(result))
						broadcast("PROPOSE:"+proposemessage)
					#s.send("Received: "+result) # remove


				# Else if we have received a propose-message, forward it to an acceptor 
				# that in turn replies with with eighter its reply if accepted, else returns
				# an empty string(?)
				elif data[0:8] == "PROPOSE:":
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
						print reply
						if reply['conflict'] != None:
							post = reply['conflict']
							posts.insert(0, post)
							# Conflict occured, add post to begining of posts, continue as normal
						del reply['conflict']
						reply = json.dumps(reply)
						broadcast("ACCEPT:"+reply)


				# Else if we have received an accept-message, forward this to the acceptor
				# which in turn broadcasts an accepted-message if it accepted the value
				elif data[0:7] == "ACCEPT:":
					result = data[7:]
					result = json.loads(result)
					reply = acceptor.receiveAccept(result)
					broadcast("ACCEPTED:"+json.dumps(reply))


				# Else if we have received an accepted-message, forward this to the proposer
				# which in turn broadcasts the decided value if all acceprors have accepted 
				# the value
				elif data[0:9] == "ACCEPTED:":
					result = data[9:]
					result = json.loads(result)
					reply = proposer.receiveAccepted(result)
					if reply == "RESTART":
						proposemessage = json.dumps(proposer.prepare(proposer.myValue)) # This makes sense?
						broadcast("PROPOSE:"+proposemessage)

					# Reply is None until majority is reached, reply is the value as a string
					elif reply != None:
						broadcast("DECIDE:"+reply)  #reply is a string

						if not posts:
							paxosRunning = False
						else:
							post = posts.pop(0)
							proposemessage = json.dumps(proposer.prepare(post)) # This makes sense
							broadcast("PROPOSE:"+proposemessage)



				# Else if we have received a decide-message, a value has been decided, forward
				# to acceptor which stores the value in the log
				elif data[0:7] == "DECIDE:":
					result = data[7:] #result is a string
					acceptor.receiveDecide(result)


				# Else if we have received a shutdown-message, end the connection and end the process
				elif data[0:8] == "SHUTDOWN":
					print 'Shutting Down'
					#server.shutdown(2)
					s.send('GOODBYE')
					server.close()
					print 'Goodbye'
					sys.exit(0)


				# Else return an invalid-message
				else:
					try:
						s.send('INVALID')
					except:
						print "lost connetion to someone2"
						if s in connections:
							connections.remove(s)

				break

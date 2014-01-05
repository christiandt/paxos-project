paxos-project
=============

In this project we have implemented a micro-blogging (Mblog) application 
that is fully replicated to many sites, using the Paxos protocol.


Our implementation of Paxos consists of 5 parts: Server, Proposer, Acceptor, Tests and Client. 

##Server
The server handles all of the communication in paxos. It interprets the received message, and forwards data to the correct function in either the proposer or acceptor. The received data starts with a keyword followed by the actual data in either JSON format from other servers, or just plain text.

Supported plain text input:
###READ: 
Returns the results of acceptor.receiveRead() back to the sender in plain text format with each post separated by a colon.

###POST: 
If Paxos is running, put post in queue, else send data to proposer.prepare(), and broadcast the result as a PROPOSE-message. This essentially starts a Paxos run.

###END: 
Close the connection to the sender, and remove it from the connections list.

###SHUTDOWN: 
Send GOINGDOWN-message, close all connections and end program. This stops the server from communications with other servers, and server.py needs to manually be restarted.

###GOINGDOWN: 
Lets other servers know that a server was shut down. Removes the connection to this server

###CATCHUP: 
When connecting to a system with already running servers, the CATCHUP-message contains the whole log so that you can catch up with the rest.

Supported JSON input:
##PROPOSE: 
A PROPOSE-message contains the proposal sent to all acceptors. The proposal data consists of the sender ID, and the proposal ID. When a PROPOSE-message is received, it is sent to acceptor.receivePropose(). The result is then sent back to the proposer as an ACK-message.

###ACK: 
An ACK-message tells the proposer whether an acceptor has accepted or rejected the proposal. It’s data contains senderID, proposalID, value, type and senderPropID. The data is sent to proposer.receivePromise(), who returns None, RESTART or conflict/no-conflict. If the returned value is None, we have not yet received ACK messages from the majority, if RESTART is returned we need to propose our own value again, if a conflict has occurred we need to put our value into the post-queue again, and lastly if no conflict is returned, we broadcast an ACCEPT-message

###ACCEPT: 
An Accept-message tells the acceptor to accept a given value. It’s data contains senderID, proposalID and value. The message data is sent to acceptor.receiveAccept(), and the result sent back to the proposer.

###ACCEPTED: 
An ACCEPTED message tells the proposer that an acceptor has accepted it’s proposed value. The message data consists of senderID, proposalID and value, which is sent to proposer.receiveAccepted(). proposer.receiveAccepted(result) has return values of eigther None, RESTART or the data to be broadcasted. If the return value is None, the proposer has not received reply from a majority, if the returnvalue is RESTART we need to propose our value over again, else a value has been decided and is broadcast as a DECIDE message.

###DECIDE: 
A DECIDE message tells the acceptors that a value has been accepted, and should be stored in it’s log. The DECIDE message data contains only a value-field with the post to be written to the log.

When the server starts, it tries to connect to a predefined list of IPs and add them to a connections list. After this is done the server enters the main while-loop. We use "select" to know when which sockets in the connections list are readable, and the program waits quietly until data is received, or a new client connects (readable data on the server socket). If a new client connects, we add it to the connections list, and send a CATCHUP-message. If a server where to crash hard without sending a GOINGDOWN-message, it will show up a readable socket. We therefore need a try-except when reading the data. We also try one more time to send a PING-message to the server, conclude that it is gone, and remove it from the connections list so that it does not interrupt the operation of the other servers. The debug-variable can be used to print out the messages received and broadcast by the server. Messages sent from the acceptor to the proposer is not printed out on the acceptor to ease debugging. This is of course printed on the proposer.


##Proposer
The Proposer is the program that is executed every time a server wants to propose a new value. It consists of the three methods prepare, receivePromise and receiveAccepted. The two variables serverID and majority is set at the beginning of this program.

###prepare
This method is initiated when a new post has arrived, or if there is more posts in the queue. It sets a new, higher proposalID based on what proposalIDs the class has encountered earlier, and returns a propose-message.

###receivePromise
This method is initiated upon receival of accepted-messages. 
Firstly, we choose to disregard old messages, i.e. messages that is not an answer to this specific proposalID.
The method returns None until majority of some kind is reached.
If we reach a majority of NACKs, we send a RESTART message.
If we reach a majority of ACKs, we have to check if we have received any previously accepted values. If so, we have to change our value to the value of the highets received proposalID, and broadcast it.
We ensure to empty the lists we use to check for majority, to make sure we don’t have old responses laying around for later executions.

###receiveAccepted
This method is initiated upon receival of accepted-messages. 
As long as majority is not reached, return None.
When majority is reached, check if any received proposalIDs are higher than ours. If it is, return RESTART, if not, return your own value (myValue) and save value to log.


##Acceptor
The Acceptor is all other servers than the Proposer. It is responsible for answering the Proposal- and Accept-messages, and writing post to log upon receival of Decide-message. It also contains the logic regarding reading and saving to the log.

getLog, saveLog, saveLogString, receiveRead

###receivePropose
If received proposalID is higher than the previously highets ID minProposal, set minProposal to proposalID. Set accepted-type to ACK, and return accepted-message.
If any previously values is in the works of getting decided, it’s info will be stored in the accepted-dictionary. If not, the values are None.
If received proposalID is lower than minProposal, return NACK-message.
In these messages the senders proposalID is added to the return-message, so that the proposer-methods can identify whether these messages are old and can be discarded.

###receiveAccept
If received proposalD is higher than minProposal, set the received accept-message to the local accepted-message, and return it. If not, return the accepted-message that was the last accepted value.

###receiveDecide
Upon receiveDecide, reset the local accepted-value, and save the proposed post to the log.


##Client
The client is a simple program that takes input from the user, and transmits the message to the server it is connected to (the server IP is defined in the TCP_IP variable). It uses raw_input to take input from the user, send the message to the server, then wait for a reply from the server. The reception of data has a timeout of one second. If the timeout is fired, we assume all data has been received. We can use timeout on the client as some potentially lost data to the client (due to >1sec. delay) does not affect Paxos. The is intended only to be used to transmit POST: READ: END and SHUTDOWN messages.


##Tests
We decided to make a simple test-class to make the initial troubleshooting and debugging a bit easier and clearer. What we made tests for:
To ensure that the ReceivePromise method in Proposer performed the correct tasks based on the received messages from the Acceptor class. I.e. that it needs majority, and what to do whether the majority consists of ACKs or NACKs, and if they are all ACKs, do any of them have a previously accepted value and proposalID.
To ensure that ReceiveAccepted in Proposer either broadcasts its own value it has the highest proposalID, or if it receives a higher ProposalID and simply returns None.
When the Acceptor receives a Proposal, we have made tests for three scenarios. 
Receives a high enough proposalID and  no previously values exist.
Received a high enough proposalID and previous value exists.
Receive a lower porposalID than previously accepted.
When the Acceptor receives an Accept-message, we have made tests for what the method should do if the received proposalID is higher than, lower than, or equal to a previously received proposalID, minProposal.


# coding=utf-8
import math, acceptor 

serverID = 3			# server ID
myValue = ""
proposalID = serverID	# ProposalID increments 10 with each prepare. Last digit is the server ID
acceptedPromise = []
acceptedAccepted = []
notAcceptedPromise = []
majority = 1
maxProposalID = 0


def prepare(post):
	global myValue
	global proposalID
	global maxProposalID
	myValue = post 		# Set the local value to the received post-message
	
	if maxProposalID != None:
	    maxProposalID += 10
	    proposalID = int(math.floor(maxProposalID/10) * 10 + serverID)	# changed back
	else:
		proposalID+=10

	propose = {'senderID': serverID, 'proposalID' : proposalID}
	return propose


def receivePromise(accepted):
	global myValue
	global acceptedPromise
	global notAcceptedPromise
	# global maxProposalID
	
	# If we receive older proposal or a NACK, it shoud not count in the majority
	if accepted['type'] == "ACK": 
		acceptedPromise.append(accepted)
	elif accepted['type'] == "NACK":
		notAcceptedPromise.append(accepted)

	# If the majority consists of rejections (NACK), add the value to the front of Paxos-queue (restart)
	if len(notAcceptedPromise) >= majority:
		notAcceptedPromise = []
		acceptedPromise = []
		return "RESTART"

	# If we have received reply from the majority
	elif len(acceptedPromise) >= majority:
		
		# Find the maximum proposal id of all the accepted promises returned from the acceptors
		maxProposalID = max(promise['proposalID'] for promise in acceptedPromise)	# Will this one handle "None"?
		for promise in acceptedPromise:
			if maxProposalID != None:
				# If not all proposal IDs are None, set myValue to the value of the proposal 
				# with the highest proposal ID
				if promise['proposalID'] == maxProposalID:
					# promise['value'] should be added to the front of the paxos queue
					myOldValue = myValue
					myValue = promise['value']
					accept = {'senderID': serverID, 'proposalID' : proposalID, 'value' : myValue, 'conflict' : myOldValue}
					# Reset the list of accepted promises when we broadcast the accept message
					notAcceptedPromise = []
					acceptedPromise = []
					return accept
		accept = {'senderID': serverID, 'proposalID' : proposalID, 'value' : myValue, 'conflict' : None}
		# Reset the list of accepted promises when we broadcast the accept message
		notAcceptedPromise = []
		acceptedPromise = []
		return accept
	return None


def receiveAccepted(accepted):
	global acceptedAccepted
	acceptedAccepted.append(accepted)

	# Require a majority
	if len(acceptedAccepted) >= majority: 
		# If we have majority, check if any of the acc-messages has a proposal ID higher than the local
		# If so, restart proposal
		for accepted in acceptedAccepted:
			if accepted['proposalID'] > proposalID:
				acceptedAccepted = []	# resets the list
				return "RESTART"
		acceptedAccepted = []
		acceptor.receiveDecide(myValue)
		return myValue
	return None


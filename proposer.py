# coding=utf-8

serverID = 3			# server ID
myValue = ""
proposalID = serverID	# ProposalID increments 10 with each prepare. Last digit is the server ID
acceptedPromise = []
acceptedAccepted = []
majority = 3

proposalNum = 2

def prepare(post):
	global proposalID
	myValue = post 		# Set the local value to the received post-message
	proposalID += 10
	propose = {'senderID': serverID, 'proposalID' : proposalID}
	return propose


def receivePromise(accepted):
	global myValue
	global acceptedPromise
	acceptedPromise.append(accepted)

	# If we have received reply from the majority
	if len(acceptedPromise) >= majority:
		# Find the maximum proposal id of all the accepted promises returned from the acceptors
		maxProposalID = max(promise['proposalID'] for promise in acceptedPromise)
		for promise in acceptedPromise:
			if maxProposalID != None:
				# If not all proposal IDs are None, set myValue to the value of the proposal 
				# with the highest proposal ID
				if promise['proposalID'] == maxProposalID:
					myValue = promise['value']
		# Reset the list of accepted promises when we broadcast the accept message
		acceptedPromise = []
		accept = {'senderID': serverID, 'proposalID' : proposalID, 'value' : myValue}
		return accept
	return None


def receiveAccepted(accepted):
	global acceptedAccepted
	acceptedAccepted.append(accepted)
	if len(acceptedAccepted) >= majority:
		# If we have majority, check if any of the acc-messages has a proposal ID higher than the local
		# If so, restart proposal
		for accepted in acceptedAccepted:
			if accepted['proposalID'] > serverID:
				acceptedAccepted = []
				return "RESTART"
		acceptedAccepted = []
		return myValue
	return None


def resetValues():
	myValue = ""
	proposalID = serverID
	acceptedPromise = []
	acceptedAccepted = []


# acc = {'senderID': None, 'proposalID' : 3, 'value' : "BestestePost"}
# acc2 = {'senderID': None, 'proposalID' : 3, 'value' : "blogtest"}
# acc3 = {'senderID': None, 'proposalID' : 3, 'value' : "bestPost"}
# print receiveAccepted(acc)
# print receiveAccepted(acc2)
# print receiveAccepted(acc3)


# acc = {'senderID': None, 'proposalID' : 9, 'value' : "BestestePost"}
# acc2 = {'senderID': None, 'proposalID' : 2, 'value' : "blogtest"}
# acc3 = {'senderID': None, 'proposalID' : 5, 'value' : "bestPost"}
# print receivePromise(acc)
# print receivePromise(acc2)
# print receivePromise(acc3)['value']


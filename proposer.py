# coding=utf-8

from proposal import *
from accept import *

myID = 3			# server ID
myValue = 7
proposalID = 0	
acceptedPromise = []
maj = 3

proposalNum = 2

def prepare(post):
	global proposalID
	blogpost = post
	proposalID += 1
	propose = proposal(myID, proposalID)
	return propose


def receivePromise(accepted):
	global myValue
	global acceptedPromise
	acceptedPromise.append(accepted)
	if len(acceptedPromise) >= maj:
		for promise in acceptedPromise:
			if promise.proposalID != None and promise.value != None:
				 myValue = max(value.value for value in acceptedPromise)
		acceptedPromise = []
		return accept(myID, proposalID, myValue)
	return None


#acc = accept(None, None, None)
#acc2 = accept(None, 5, 6)
#acc3 = accept(None, None, None)
#print receivePromise(acc)
#print receivePromise(acc2)
#print receivePromise(acc3).value




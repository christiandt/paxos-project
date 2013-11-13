# coding=utf-8
__author__ = 'Kine'

proposalID = None
acceptedProposal = None
acceptedValue = None



def receivePrepare(self, senderID, proposalID):
    global minProposal
    if proposalID > minProposal:
        minProposal = proposalID
        # Do send/return stuff
    if proposalID == self.proposalID:
        # Do send/return stuff      return acceptedProposal, acceptedValue


def receiveAcceptRequest(self, senderID, proposalID, value):
    if proposalID >= self.proposalID:
        self.proposalID = proposalID
        self.acceptedProposal = proposalID
        self.acceptedValue = value
    return self.proposalID


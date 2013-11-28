# coding=utf-8

import cPickle as pickle
from proposal import *
from accept import *

minProposal = None
accepted = accept(None, None, None)


def getLog():
    try:
        logFile = open("log.p", "rb")
        log = pickle.load(logFile)
        logFile.close
        return log
    except:
        return ["!"]


def saveLog(log):
    try:
        logFile = open("log.p", "wb")
        pickle.dump(log, logFile)
        logFile.close
        return True
    except:
        return False


def receiveRead():
    logString = ""
    for post in getLog():
        logString += (post+":")
    return logString[0:-1]


def receivePrepare(proposed):
    global minProposal
    if proposed.proposalID >= minProposal:
        minProposal = proposed.proposalID
    return accepted


def receiveAccept(accept):
    if accept.proposalID >= minProposal:
        accepted = accept
    return accepted


def receiveDecide(result):
    log = getLog()
    log.append(data)
    if saveLog(log):
        return "SUCCESS"
    else:
        return "FAIL"
    None






# Is this section needed anymore?


#proposalID
#acceptedProposal
#acceptedValue

#     if proposed.proposalID > minProposal:
#         minProposal = proposalID
#         # Do send/return stuff
#     if proposed.proposalID == proposalID:
#         None
#         # Do send/return stuff      return acceptedProposal, acceptedValue


# def receiveAcceptRequest(senderID, proposalID, value):
#     if proposalID >= self.proposalID:
#         self.proposalID = proposalID
#         self.acceptedProposal = proposalID
#         self.acceptedValue = value
#     return self.proposalID


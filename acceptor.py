# coding=utf-8

import cPickle as pickle

minProposal = 0
accepted = {'senderID': None, 'proposalID' : None, 'value' : None}


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


def receivePropose(proposed):
    global minProposal
    global accepted
    # If we receive a proposal with an ID higher than (or eq) what as allready been proposed,
    # reply back to proposer with ID None to indicate that we are committing to this proposal
    if proposed['proposalID'] > minProposal:
        minProposal = proposed['proposalID']
        accepted['type'] = "ACK"
        return accepted
    # If the received ID is lower than what has allready been proposed, reply back to proposer
    # with the last accepted value
    else:
        return {'senderID': None, 'proposalID' : None, 'value' : None, 'type': "NACK"}


def receiveAccept(accept):
    global accepted
    # If the received ID is higher than (or eq) the local ID, set the local ID to the received ID
    # and broadcast the accepted value
    if accept['proposalID'] >= minProposal:
        accepted = accept
    # If not, we broadcast the last accepted value
    return accepted


def receiveDecide(result):
    global accepted
    print "Decided: ", result
    accepted = {'senderID': None, 'proposalID' : None, 'value' : None}
    log = getLog()
    log.insert(0, result)
    saveLog(log)


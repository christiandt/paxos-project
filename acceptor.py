# coding=utf-8

import cPickle as pickle

minProposal = None
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


def receivePrepare(proposed):
    global minProposal
    if proposed['proposalID'] >= minProposal:
        minProposal = proposed['proposalID']
        return {'senderID': None, 'proposalID' : None, 'value' : None}
    else:
        return accepted


def receiveAccept(accept):
    # If the received ID is higher than the local ID, set the local ID to the received ID
    if accept['proposalID'] >= minProposal:
        accepted = accepted
    return accepted


def receiveDecide(result):
    log = getLog()
    log.append(data)
    if saveLog(log):
        return "SUCCESS"
    else:
        return "FAIL"


def resetValues():
    global accepted
    accepted = {'senderID': None, 'proposalID' : None, 'value' : None}

minProposal = 55
accepted = {'senderID': None, 'proposalID' : 54, 'value' : "Works"}
propose = {'senderID': None, 'proposalID' : 33}

print receivePrepare(propose)



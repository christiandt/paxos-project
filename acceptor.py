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
        
    # TEST:
    # receive a high proposalID when blank
    # receive a high proposalID when have previously accepted something
    # receive a proposalID that is lower than minProposal (i.e. lower than a prev. proposalID)


def receiveAccept(accept):
    # If the received ID is higher than (or eq) the local ID, set the local ID to the received ID
    # and broadcast the accepted value
    if accept['proposalID'] >= minProposal:
        accepted = accept
    # If not, we broadcast the last accepted value
    return accepted

    # Test:
    # receive accept where proposalID is higher/lower/equal to minProposal

def receiveDecide(result):
    log = getLog()
    log.append(data)
    if saveLog(log):
        return "SUCCESS"
    else:
        return "FAIL"



# minProposal = 28
# accepted = {'senderID': None, 'proposalID' : 29, 'value' : "Last accepted"}
# propose = {'senderID': None, 'proposalID' : 30, 'value' : "New Accept"}

# print receiveAccept(propose)



# minProposal = 55
# accepted = {'senderID': None, 'proposalID' : 54, 'value' : "Works"}
# propose = {'senderID': None, 'proposalID' : 33}

# print receivePrepare(propose)



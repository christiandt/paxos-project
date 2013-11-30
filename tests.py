import unittest
import proposer
import acceptor


class paxosTests(unittest.TestCase):

	def setUp(self):
		None


	def test_Post(self):
		global proposer
		blogpost = "test"
		proposal = {'senderID': 3, 'proposalID' : 13}
		self.assertEqual(proposal, proposer.prepare(blogpost))


		# Proposer discards self-value since received others from acceptor, sets its value to highest
	def test_proposerReceivePromise_allACK_withValue(self):
		acc = {'proposalID' : 9, 'value' : "BestestePost", 'type' : "ACK"}
		acc2 = {'proposalID' : 2, 'value' : "blogtest", 'type' : "ACK"}
		acc3 = {'proposalID' : 5, 'value' : "bestPost", 'type' : "ACK"}
		proposer.receivePromise(acc)
		proposer.receivePromise(acc2)
		self.assertEqual(acc['value'], proposer.receivePromise(acc3)['value'])


		# Proposer gets majority of ACK, none with proposalIDs, returns its own value
	def test_proposerReceivePromise_allACK_withoutValue(self):
		proposer.proposalID = 34
		acc1 = {'proposalID' : None, 'value' : None, 'type' : "ACK"}
		acc2 = {'proposalID' : None, 'value' : None, 'type' : "ACK"}
		acc3 = {'proposalID' : None, 'value' : None, 'type' : "ACK"}
		proposer.receivePromise(acc1)
		proposer.receivePromise(acc2)
		self.assertEqual(proposer.proposalID, proposer.receivePromise(acc3)['proposalID'])


		# When received majority of NACKs, give up / restart
	def test_proposerReceivePromise_allNACK(self):
		nacc = {'proposalID' : None, 'value' : None, 'type' : "NACK"}		
		nacc1 = {'proposalID' : None, 'value' : None, 'type' : "NACK"}		
		nacc2 = {'proposalID' : None, 'value' : None, 'type' : "NACK"}
		proposer.receivePromise(nacc)
		proposer.receivePromise(nacc1)
		self.assertEqual("RESTART", proposer.receivePromise(nacc2))


		# Behaviour when receive both NACK and ACK, maj of ACK in last round
	def test_proposerReceivePromise_misc(self):
		acc1 = {'proposalID' : None, 'value' : None, 'type' : "ACK"}
		acc2 = {'proposalID' : None, 'value' : None, 'type' : "ACK"}
		acc3 = {'proposalID' : 9, 'value' : "BestestePost", 'type' : "ACK"}
		nacc1 = {'proposalID' : None, 'value' : None, 'type' : "NACK"}
		nacc2 = {'proposalID' : None, 'value' : None, 'type' : "NACK"}
		proposer.receivePromise(acc1)
		proposer.receivePromise(acc2)
		proposer.receivePromise(nacc1)
		proposer.receivePromise(nacc2)
		self.assertEqual(acc3['value'], proposer.receivePromise(acc3)['value'])


	def test_proposerReceiveAccepted(self):
		proposer.myValue = "Kine er kul"
		acc = {'proposalID' : 12, 'value' : "BestestePost"}
		acc2 = {'proposalID' : 2, 'value' : "blogtest"}
		acc3 = {'proposalID' : 5, 'value' : "bestPost"}
		acc4 = {'proposalID' : 13, 'value' : "bestPost"}
		proposer.receiveAccepted(acc)
		proposer.receiveAccepted(acc2)
		
		# Returns its own value when none other has higher ProposalID
		self.assertEqual(proposer.myValue, proposer.receiveAccepted(acc3))

		# Returns None when other receival has highet ProposalID
		self.assertEqual(None, proposer.receiveAccepted(acc4))


		# When proposalID is higher, and none previous values
	def test_acceptorReceivePropose_withNonePrevious(self):
		acceptor.minProposal = 5
		acceptor.accepted = {'proposalID' : None, 'value' : None}
		prop = {'proposalID' : 17}
		self.assertEqual(acceptor.accepted, acceptor.receivePropose(prop))


		# When proposalID is higher, and previous values exists
	def test_acceptorReceivePropose_withPreviousValues(self):
		acceptor.minProposal = 19
		acceptor.accepted = {'proposalID' : 19, 'value' : "I am previous"}
		prop = {'proposalID' : 20}
		self.assertEqual(acceptor.accepted, acceptor.receivePropose(prop))


		# When ProposalID is too low, and NACK shall be returned
	def test_acceptorReceivePropose_withLowID(self):
		acceptor.minProposal = 19
		acceptor.accepted = {'proposalID' : 19, 'value' : "I am previous"}
		prop = {'proposalID' : 17}
		self.assertEqual("NACK", acceptor.receivePropose(prop)['type'])


	def test_acceptorReceiveAccept(self):
		acceptor.minProposal = 12
		acceptor.accepted = {'proposalID' : 12, 'value' : "I am previously accepted"}
		acc1 = {'proposalID' : 11, 'value' : "EnPost"}
		acc2 = {'proposalID' : 12, 'value' : "ToPost"}
		acc3 = {'proposalID' : 13, 'value' : "TrePost"}

		# When received proposalID is lower then minProposal
		self.assertEqual(acceptor.minProposal, acceptor.receiveAccept(acc1)['proposalID'])

		# When received proposalID is equal to minProposal
		self.assertEqual(acc2['proposalID'], acceptor.receiveAccept(acc2)['proposalID'])
		
		# When received proposalID is greater then minProposal
		self.assertEqual(acc3['proposalID'], acceptor.receiveAccept(acc3)['proposalID'])


	def test_acceptorReceiveDecide(self):
		None


if __name__ == '__main__':
    unittest.main()

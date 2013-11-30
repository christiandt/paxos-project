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


		# Proposer discards self-value since received others from acceptor
	def test_proposerReceivePromise_allACK_withValue(self):
		acc = {'senderID': None, 'proposalID' : 9, 'value' : "BestestePost", 'type' : "ACK"}
		acc2 = {'senderID': None, 'proposalID' : 2, 'value' : "blogtest", 'type' : "ACK"}
		acc3 = {'senderID': None, 'proposalID' : 5, 'value' : "bestPost", 'type' : "ACK"}
		proposer.receivePromise(acc)
		proposer.receivePromise(acc2)
		self.assertEqual(acc['value'], proposer.receivePromise(acc3)['value'])


	def test_proposerReceivePromise_allACK_withoutValue(self):
		proposer.proposalID = 34
		acc1 = {'senderID': None, 'proposalID' : None, 'value' : None, 'type' : "ACK"}
		acc2 = {'senderID': None, 'proposalID' : None, 'value' : None, 'type' : "ACK"}
		acc3 = {'senderID': None, 'proposalID' : None, 'value' : None, 'type' : "ACK"}
		proposer.receivePromise(acc1)
		proposer.receivePromise(acc2)
		self.assertEqual(proposer.proposalID, proposer.receivePromise(acc3)['proposalID'])

		# When received majority of NACKs, give up / restart
	def test_proposerReceivePromise_allNACK(self):
		nacc = {'senderID': None, 'proposalID' : None, 'value' : None, 'type' : "NACK"}		
		nacc1 = {'senderID': None, 'proposalID' : None, 'value' : None, 'type' : "NACK"}		
		nacc2 = {'senderID': None, 'proposalID' : None, 'value' : None, 'type' : "NACK"}
		proposer.receivePromise(nacc)
		proposer.receivePromise(nacc1)
		self.assertEqual("RESTART", proposer.receivePromise(nacc2))


		# Behaviour when receive both NACK and ACK, maj of ACK
	def test_proposerReceivePromise_misc(self):
		acc1 = {'senderID': None, 'proposalID' : None, 'value' : None, 'type' : "ACK"}
		acc2 = {'senderID': None, 'proposalID' : None, 'value' : None, 'type' : "ACK"}
		acc3 = {'senderID': None, 'proposalID' : 9, 'value' : "BestestePost", 'type' : "ACK"}
		nacc1 = {'senderID': None, 'proposalID' : None, 'value' : None, 'type' : "NACK"}
		nacc2 = {'senderID': None, 'proposalID' : None, 'value' : None, 'type' : "NACK"}
		proposer.receivePromise(acc1)
		proposer.receivePromise(acc2)
		proposer.receivePromise(nacc1)
		proposer.receivePromise(nacc2)
		self.assertEqual(acc3['value'], proposer.receivePromise(acc3)['value'])




	def test_proposerReceiveAccepted(self):
		proposer.myValue = "Kine er kul"
		acc = {'senderID': None, 'proposalID' : 12, 'value' : "BestestePost"}
		acc2 = {'senderID': None, 'proposalID' : 2, 'value' : "blogtest"}
		acc3 = {'senderID': None, 'proposalID' : 5, 'value' : "bestPost"}
		acc4 = {'senderID': None, 'proposalID' : 13, 'value' : "bestPost"}
		proposer.receiveAccepted(acc)
		proposer.receiveAccepted(acc2)
		
		result = proposer.receiveAccepted(acc3)
		self.assertEqual(proposer.myValue, result)
		
		result2 = proposer.receiveAccepted(acc4)
		self.assertEqual(None, result2)



	def test_acceptorReceivePropose(self):
		None


	def test_acceptorReceiveAccept(self):
		None


	def test_acceptorReceiveDecide(self):
		None


if __name__ == '__main__':
    unittest.main()

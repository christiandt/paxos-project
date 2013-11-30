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


	def test_proposerReceivePromise(self):
		acc = {'senderID': None, 'proposalID' : 9, 'value' : "BestestePost", 'type' : "ACK"}
		acc2 = {'senderID': None, 'proposalID' : 2, 'value' : "blogtest", 'type' : "ACK"}
		acc3 = {'senderID': None, 'proposalID' : 5, 'value' : "bestPost", 'type' : "ACK"}
		proposer.receivePromise(acc)
		proposer.receivePromise(acc2)
		self.assertEqual(acc['value'], proposer.receivePromise(acc3)['value'])


	def test_proposerReceiveAccepted(self):
		None


	def test_acceptorReceivePropose(self):
		None


	def test_acceptorReceiveAccept(self):
		None


	def test_acceptorReceiveDecide(self):
		None


if __name__ == '__main__':
    unittest.main()
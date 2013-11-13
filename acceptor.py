# coding=utf-8
__author__ = 'Kine'


# Phase Prepare - COHORT

# Upon receive (“prepare”, bal) from i
# if bal ≥ BallotNum then
# BallotNum ← bal
# send (“ack”, bal, AcceptNum, AcceptVal) to i

# Phase Accept - COHORT

# Upon receive (“accept”, b, v) if b ≥ BallotNum then
# AcceptNum ← b; AcceptVal ← v proposal */
# ￼/* accept send (“accept”, b, v) to all (first time only)


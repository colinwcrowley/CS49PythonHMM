# Note that the class does not generate outcomes, but rather tells you
# the likely hood of given outcomes. I though this was a reasonable
# implementation choice since we are only interested in EXPLAINGING an
# observation sequence. We aren't trying to generate one.


class HMM(object):
    def __init__(self, Q, V):
        self.Q = Q  # Q is the list of states
        self.V = V  # V is the alphabet of symbols observed
        self.N = len(Q)
        self.M = len(V)
        self.A = [[0 for i in range(N)] for i in range(N)]
        # A is the N x N transition matrix
        self.B = [[0 for i in range(N)] for i in range(M)]
        # B is the N x M matrix of probabilities for observing each
        # symbol in a given state
        self.pi = [0 for i in range(N)]
        # pi is the initial state probability distribution

    def probabilityOfObservation(self, O):
        # O is the list of observations, for which we will return the
        # probability that they occur.
        print "test"

    def mostLikelyStateSequence(self, O):
        # O is the list of observations, for which we will return the
        # most likely state sequence
        print "test"

    def trainModel(self, O):
        # O is the list of observations, with which we will adjust the
        # parameters of the model to maximize the probability that they
        # occur. You have to train the model, or else A, B, and pi won't
        # be set.
        print "test"

    # These setters are for debuging purposes
    def setA(self, A):
        self.A = A

    def setB(self, B):
        self.B = B

    def setPiB(self, pi):
        self.pi = pi

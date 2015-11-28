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
        self.A = [[0 for i in range(self.N)] for i in range(self.N)]
        # A is the N x N transition matrix
        self.B = [[0 for i in range(self.N)] for i in range(self.M)]
        # B is the N x M matrix of probabilities for observing each
        # symbol in a given state
        self.pi = [0 for i in range(self.N)]
        # pi is the initial state probability distribution

    def alpha(self, O, t, i):
        # forward probability recursively defined
        if t is 0:
            return self.pi[i] * self.B[i][self.V.index(O[0])]
        sumOfPathProbs = 0
        for h in range(self.N):
            sumOfPathProbs += self.alpha(O, t-1, h) * self.A[h][i]
        return sumOfPathProbs * self.B[i][self.V.index(O[t])]

    def beta(self, O, t, i):
        # backwards probability recursively defined
        if t is len(O)-1:
            return 1
        sumOfPathProbs = 0
        for h in range(self.N):
            sumOfPathProbs += self.A[i][h] * self.B[h][self.V.index(O[t+1])] * self.beta(O, t+1, h)
        return sumOfPathProbs

    def probabilityOfObservation(self, O):
        # O is the list of observations (indecies), for which we will
        # return the probability that they occur.
        prob = 0
        for i in range(self.N):
            prob += self.alpha(O, len(O)-1, i)
        return prob

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

    def setPi(self, pi):
        self.pi = pi

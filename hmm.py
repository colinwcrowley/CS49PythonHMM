# I want an example to work with as we build this thing, and we can use
# the weather example because that was for plain old Markov chain. So I
# feel like a better example would be the mood of some professor and the
# grade the the grade that she give. (i.e. when arngy she gives lower
# grades and when happy she gives higher grades)


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

    def printA(self):
        print self.A

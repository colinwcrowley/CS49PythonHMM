# Note that the class does not generate outcomes, but rather tells you
# the likely hood of given outcomes. I though this was a reasonable
# implementation choice since we are only interested in EXPLAINGING an
# observation sequence. We aren't trying to generate one.

# helper functions
def maximum(func, a, b):
    num = 0
    for i in range(a, b):
        cur = func(i)
        if cur > num:
            num = cur
    return num

def argmax(func, a, b):
    num = func(a)
    index = a
    for i in range(a+1, b):
        cur = func(i)
        if cur > num:
            num = cur
            index = i
    return index


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

    def gamma(self, O, t, i):
        # probability that we are in some state at some time given an
        # odservation sequence
        probOfObservation = 0
        for h in range(self.N):
            probOfObservation += self.alpha(O, t, h) * self.beta(O, t, h)
        return self.alpha(O, t, i) * self.beta(O, t, i) / probOfObservation

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

        # Implementing this with bottem up dynamic programming. So both
        # delta and psi will be 2-D arrays, and we can just loop
        # through them to keep track of the previous values
        delta = [[0 for i in range(self.N)] for i in range(len(O))]
        psi = [[0 for i in range(self.N)] for i in range(len(O))]

        # initialization of delta
        for i in range(self.N):
            delta[0][i] = self.pi[i] * self.B[i][self.V.index(O[1])]

        print " -> delta array after initialization:", delta

        for t in range(1, len(O)):
            for i in range(self.N):
                lam = lambda x: delta[t-1][x]*self.A[x][i] # lambdas ftw
                delta[t][i] = maximum(lam, 0, self.N) * self.B[i][self.V.index(O[t])]
                psi[t][i] = argmax(lam, 0, self.N)


        print " -> finished delta array:", delta
        # now that we've covered all of the possibilities, let's choose
        # the best one.

        lam2 = lambda x: delta[len(O)-1][x]
        pStar = maximum(lam2, 0, self.N)
        qStar = argmax(lam2, 0, self.N)

        # now let's build our array to return
        path = [self.Q[qStar]]
        lastIndex = qStar
        for t in reversed(range(len(O)-1)):
            path.insert(0, self.Q[psi[t+1][lastIndex]])
            lastIndex = psi[t+1][lastIndex]

        return path

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

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


def doubleSummation(func, a, b, x, y):
    num = 0
    for i in range(a, b):
        for j in range(x, y):
            num += func(i, j)
    return num


def summation(func, a, b):
    num = 0
    for i in range(a, b):
        num += func(i)
    return num


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

    def alphaDynamicSet(self, O):
        # Use dynamic programing to make a table at the begining and
        # reference it in the following calculations.
        self.alphaArray = [[0 for i in range(self.N)] for i in range(len(O))]
        for i in range(self.N):
            self.alphaArray[0][i] = self.pi[i] * self.B[i][self.V.index(O[0])]
        for t in range(1, len(O)):
            for i in range(self.N):
                sumOfPathProbs = 0
                for h in range(self.N):
                    sumOfPathProbs += self.alphaArray[t-1][h] * self.A[h][i]
                self.alphaArray[t][i] = sumOfPathProbs * self.B[i][self.V.index(O[t])]


    def alphaDynamicGet(self, t, i):
        return self.alphaArray[t][i]

    def beta(self, O, t, i):
        # backwards probability recursively defined
        if t is len(O)-1:
            return 1
        sumOfPathProbs = 0
        for h in range(self.N):
            sumOfPathProbs += self.A[i][h] * self.B[h][self.V.index(O[t+1])] * self.beta(O, t+1, h)
        return sumOfPathProbs

    def betaDynamicSet(self, O):
        # Use dynamic programing to make a table at the begining and
        # reference it in the following calculations.
        self.betaArray = [[0 for i in range(self.N)] for i in range(len(O))]
        for i in range(self.N):
            self.betaArray[len(O)-1][i] = 1
        for t in reversed(range(0, len(O)-1)):
            for i in range(self.N):
                sumOfPathProbs = 0
                for h in range(self.N):
                    sumOfPathProbs += self.A[i][h] * self.B[h][self.V.index(O[t+1])] * self.betaArray[t+1][h]
                self.betaArray[t][i] = sumOfPathProbs

    def betaDynamicGet(self, t, i):
        return self.betaArray[t][i]

    def gamma(self, O, t, i):
        # probability that we are in some state at some time given an
        # odservation sequence
        probOfObservation = 0
        for h in range(self.N):
            probOfObservation += self.alphaDynamicGet(t, h) * self.betaDynamicGet(t, h)
        return self.alphaDynamicGet(t, i) * self.betaDynamicGet(t, i) / probOfObservation

    def gammaDynamicSet(self, O):
        # Use dynamic programing to make a table at the begining and
        # reference it in the following calculations.

        # probability that we are in some state at some time given an
        # odservation sequence
        self.gammaArray = [[0 for i in range(self.N)] for t in range(len(O))]
        for t in range(len(O)):
            for i in range(self.N):
                probOfObservation = 0
                for h in range(self.N):
                    probOfObservation += self.alphaDynamicGet(t, h) * self.betaDynamicGet(t, h)
                self.gammaArray[t][i] = self.alphaDynamicGet(t, i) * self.betaDynamicGet(t, i) / probOfObservation

    def gammaDynamicGet(self, t, i):
        return self.gammaArray[t][i]

    def zeta(self, O, t, i, j):
        self.alphaDynamicSet(O)
        self.betaDynamicSet(O)
        num = 0
        #for a in range(self.N):
        #    for b in range(self.N):
        #        num += self.alphaDynamicGet(t, a) * self.A[a][b] * self.B[b][self.V.index(O[t+1])] * self.betaDynamicGet(t+1, b)
        for k in range(self.N):
            num += self.alphaDynamicGet(len(O)-1, k)
        return self.alphaDynamicGet(t, i) * self.A[i][j] * self.B[j][self.V.index(O[t+1])] * self.betaDynamicGet(t+1, j) / num


    def probabilityOfObservation(self, O):
        # O is the list of observations (indecies), for which we will
        # return the probability that they occur.
        # one two three
        self.alphaDynamicSet(O)
        prob = 0
        for i in range(self.N):
            prob += self.alphaDynamicGet(len(O)-1, i)
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


        for t in range(1, len(O)):
            for i in range(self.N):
                lam = lambda x: delta[t-1][x]*self.A[x][i]
                delta[t][i] = maximum(lam, 0, self.N) * self.B[i][self.V.index(O[t])]
                psi[t][i] = argmax(lam, 0, self.N)


        # Now that we've covered all of the possibilities, let's choose
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

    def interateBaumWelch(self, O):
        newPi = [self.gammaDynamicGet(0, i) for i in range(self.N)]

        newA = [[0 for i in range(self.N)] for i in range(self.N)]

        for i in range(self.N):
            for j in range(self.N):
                num = 0
                for t in range(len(O)-1):
                    num += self.zeta(O, t, i, j)
                num2 = 0
                for t in range(len(O)-1):
                    num2 += self.gammaDynamicGet(t, i)
                newA[i][j] = num/num2

        newB = [[0 for i in range(len(self.V))] for i in range(self.N)]

        for j in range(self.N):
            for k in range(len(self.V)):
                num = 0
                for t in range(len(O)):
                    if O[t] is self.V[k]:
                        num += self.gammaDynamicGet(t, j)
                num2 = 0
                for t in range(len(O)):
                    num2 += self.gammaDynamicGet(t, j)
                newB[j][k] = num/num2

        self.pi = newPi
        self.A = newA
        self.B = newB

        #Now just normalize each matrix
        for i in range(self.N):
            rowSum = 0
            for j in range(self.N):
                rowSum += self.A[i][j]
            for j in range(self.N):
                self.A[i][j] = self.A[i][j] / rowSum

        for i in range(self.N):
            rowSum = 0
            for k in range(len(self.V)):
                rowSum += self.B[i][k]
            for k in range(len(self.V)):
                self.B[i][k] = self.B[i][k] / rowSum

    def trainModel(self, O, epsilon):
        # O is the list of observations, with which we will adjust the
        # parameters of the model to maximize the probability that they
        # occur. You have to train the model, or else A, B, and pi won't
        # be set.
        self.alphaDynamicSet(O)
        self.betaDynamicSet(O)
        self.gammaDynamicSet(O)
        done = False
        forwardBackwardProbability = self.probabilityOfObservation(O)
        print "Intitial fb: ", forwardBackwardProbability
        while not done:
            self.interateBaumWelch(O)
            if abs(forwardBackwardProbability - self.probabilityOfObservation(O)) / forwardBackwardProbability < epsilon:
                done = True
            forwardBackwardProbability = self.probabilityOfObservation(O)
            print "fb: ", forwardBackwardProbability
            #print "B val:", self.B
        print "done"

    # These setters are for debuging purposes
    def setA(self, A):
        self.A = A

    def setB(self, B):
        self.B = B

    def setPi(self, pi):
        self.pi = pi

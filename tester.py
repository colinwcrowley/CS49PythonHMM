# I want an example to work with as we build this thing, and we can use
# the weather example because that was for plain old Markov chain. So I
# feel like a better example would be the mood of some professor and the
# grade the the grade that she give. (i.e. when arngy she gives lower
# grades and when happy she gives higher grades)

execfile("hmm.py")

states = ["angry", "sad", "happy"]
symbols = ["A", "B", "C", "D", "F"]

hmm = HMM(states, symbols)


hmm.setA([[0.5, 0.25, 0.25],  # if she's angry, she'll probably stay angry
          [0.3, 0.3, 0.4],  # but she usualy cheers up after she's sad
          [0.1, 0.4, 0.5]])  # happy makes more happy :)

hmm.setB([[0.05, 0.15, 0.2, 0.25, 0.35],  # she ain't nice when angry!
          [0.1, 0.6, 0.1, 0.1, 0.1],  # "don't feel like grading, I'll give em all B's"
          [0.4, 0.2, 0.2, 0.1, 0.1]])  # "I have such wonderful smart students :D"

hmm.setPi([0, 0, 1])  # happy at the begining of the year

# In this observation, the teacher only gives A's. We should therefore
# expect the emmision matrix (B) to have high numbers in the first
# column
testArray = ["A", "A", "A", "A"]

print "ALL A OBSERVATION"

hmm.trainModel(testArray, 0.002)  # 0.002 percent threashold

print "A = ", hmm.A
print "B = ", hmm.B
print "Pi = ", hmm.pi

# In this observation, the teacher switches between giving A's and
# giving F's. We should see a high probability of a self loop in both
# HAPPY and ANGRY, and high probability of emiting A's and F's
# respectively (i.e. large values in the upper left and lower right
# corners of A and large values in the upper right and lower left
# corners of B.

testArray2 = ["A", "A", "A", "A", "A", "A", "A", "A", "F", "F", "F", "F",
        "F", "F", "F", "F", "F"]

print "A/F OBSERVATION"

hmm2 = HMM(states, symbols)

hmm2.setA([[0.5, 0.25, 0.25],  # if she's angry, she'll probably stay angry
          [0.3, 0.3, 0.4],  # but she usualy cheers up after she's sad
          [0.1, 0.4, 0.5]])  # happy makes more happy :)

hmm2.setB([[0.05, 0.15, 0.2, 0.25, 0.35],  # she ain't nice when angry!
          [0.1, 0.6, 0.1, 0.1, 0.1],  # "don't feel like grading, I'll give em all B's"
          [0.4, 0.2, 0.2, 0.1, 0.1]])  # "I have such wonderful smart students :D"

hmm2.setPi([0, 0, 1])  # happy at the begining of the year

hmm2.trainModel(testArray2, 0.002)  # 0.002 percent threashold

print "A = ", hmm2.A
print "B = ", hmm2.B
print "Pi = ", hmm2.pi

# For this final test we will set the model with uniformly parameters
# for A, B, and Pi, and train it with a uniformly random observation. If
# it works correctly, there should be little change because the model is
# already at a global maximum. (There my be some overfitting to the
# random data in B, but it should not be much!)

hmm3 = HMM(states, symbols)

hmm3.setA([[0.33, 0.33, 0.33],
          [0.33, 0.33, 0.33],
          [0.33, 0.33, 0.33]])

hmm3.setB([[0.2, 0.2, 0.2, 0.2, 0.2],
          [0.2, 0.2, 0.2, 0.2, 0.2],
          [0.2, 0.2, 0.2, 0.2, 0.2]])

hmm3.setPi([0.33, 0.33, 0.33])

import random
testArray3 = [random.choice(symbols) for i in range(100)]

hmm3.trainModel(testArray3, 0.002)

print "A = ", hmm3.A
print "B = ", hmm3.B
print "Pi = ", hmm3.pi

# And now for a quick test of the forwards backwards algorith. It should make two
# observation sequences equally likely with the hmm3.

viterbiArray1 = ["A", "A", "A", "A"]
viterbiArray2 = ["F", "F", "F", "F"]
print "Forwards-Backards of hmm3: ", hmm3.probabilityOfObservation(viterbiArray1), " should equal ON AVERAGE ", hmm3.probabilityOfObservation(viterbiArray2)

#Run this a few times to see that they are indeed equal on average.

# To test the Viterbi algorithm, we should first get the most likely
# sequence of happy, happy, happy, from giving hmm2 ["A", "A", "A" ]

print "Most likely to give A, A, A, in hmm2: ", hmm2.mostLikelyStateSequence(["A", "A", "A"])

# We should also get that the most likely to produce F, F, F in
# hmm2 should go from happy to angry. This is because we start in happy,
# so the best way to get the most F's is to progress to angry

print "Most likely to give F, F, F, in hmm2: ", hmm2.mostLikelyStateSequence(["F", "F", "F"])

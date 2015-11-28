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

hmm.setPi([0.3, 0.3, 0.4])  # maybe happy at the begining of the year???

print hmm.probabilityOfObservation(["A", "B", "A"])
print hmm.beta(["A", "B", "A"], 0, 1)

# sanity check to see that the probabilities add up to 1
sum = 0
for i in symbols:
    for j in symbols:
        for k in symbols:
            sum += hmm.probabilityOfObservation([i, j, k])
print "The sum is: "
print sum

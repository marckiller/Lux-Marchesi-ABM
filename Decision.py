from random import choices

class Decision:
    """This class contain only one staticmethod 'decide'. It takes probability value as and input and returns True with that probality (False in other case)"""

    @staticmethod
    def decide(probability):
        """Takes probability, and returns True with given probability and False in other case"""
        if probability<=1:
            prob = probability
        else:
            print("Probability bigger than 1. default preobability = 0.5")
            prob = 0.5
        a = choices(population=[1, 0], weights=[prob, 1.0-prob])
        return a[0]



p1 = 0.1
p2 = 0.3
choice = [1,2, 3]
cum_weights = [p1,p2, 1 - p1 - p2]

counter = 0
for i in range(10000):
    if choices(choice, cum_weights)[0] == 1:
        counter += 1
print(counter/10000)

choice = ['optimist', 'pessimist', 'fundamentalis']
weights = [p1, p2, 1 - p1 - p2]
a = choices(choice, weights)[0]
print(a)



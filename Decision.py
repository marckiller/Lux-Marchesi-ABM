#currently not in use
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


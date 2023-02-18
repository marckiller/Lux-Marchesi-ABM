from copy import deepcopy
from Functions import Functions
from Decision import Decision
from random import choices

class Agent:

    def __init__(self, id, agnet_type = 'fundamentalist'):
        self.__id = id
        if agnet_type not in ['fundamentalist', 'noise_optimist', 'noise_pessimist']:
            self.__type = 'fundamentalist'
        else:
            self.__type = agnet_type

    def __str__(self) -> str:
        return f"Hello! I'm agent {self.get_id}, and I'm {self.type}"
        
    @property
    def get_id(self): return deepcopy(self.__id)

    @property
    def type(self): return deepcopy(self.__type)

    @type.setter
    def type(self, type): 
        if type not in ['fundamentalist', 'noise_optimist', 'noise_pessimist']:
            print(f"Agent {self.get_id} is now fundamentalist (Wrong type passed (not fundamentalist, noise_optimist or noise_pessimist)")
            self.__type = 'fundamentalist'
        else:
            self.__type = type 

    #I've decided that agent decide wether they change their mind during time iteration or not. It recives just a list of probabilities where 
    # 0: opt -> pes
    # 1: pes -> opt
    # 2: opt -> fund
    # 3: pes -> fund
    # 4: fund -> opt
    # 5: fund -> pes
    def rethink_strategy(self,prob): #it could count all probabilities based on state of the market but this is more efficient way of computing it
        """Function gets a list of probabilities that:
            0: opt -> pes
            1: pes -> opt
            2: opt -> fund
            3: pes -> fund
            4: fund -> opt
            5: fund -> pes 
        Based on that it changes agents mood and stratedy"""

        choice = ['optimist', 'pessimist', 'fundamentalis']

        if self.__type == 'fundamentalist':
            weights = [prob[4], prob[5], 1-prob[5]-prob[4]]
            self.type(choices(choice, weights)[0])

        elif self.__type == 'optimist':
            weights = [1-prob[2]-prob[0], prob[0], prob[2]]
            self.type(choices(choice, weights)[0])

        elif self.__type == 'pessimist':
            weights = [prob[1], 1-prob[1]-prob[3], prob[3]]
            self.type(choices(choice, weights)[0])

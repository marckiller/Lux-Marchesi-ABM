from copy import deepcopy

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

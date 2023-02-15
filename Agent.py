from copy import deepcopy

class Agent:

    def __init__(self, id, agnet_type = 'fundamentalist'):
        self.__id = id

        if agnet_type not in ['fundamentalist', 'noise_optimist', 'noise_pessimist']:
            self.__type = 'fundamentalist'
        else:
            self.__type = agnet_type
        
    @property
    def get_id(self): return deepcopy(self.__id)

    @property
    def type(self): return deepcopy(self.__type)

    @type.setter
    def type(self, type): 
        if type not in ['fundamentalist', 'noise_optimist', 'noise_pessimist']:
            print(f"Agent {self.get_id} is now fundamentalist (default type). Wrong type passed (not fundamentalist, noise_optimist or noise_pessimist")
            self.__type = 'fundamentalist'
        else:
            self.__type = type 


#test 

a = Agent(0, agnet_type='noise_optimist')
print(f"hello I'm agnet {a.get_id} and I'm {a.type}")

b = Agent(1)
print(f"hello I'm agnet {b.get_id} and I'm {b.type}")

c= Agent(2, agnet_type='aaaa')
print(f"hello I'm agnet {c.get_id} and I'm {c.type}")

c.type = 'noise_pessimist'
print(f"hello I'm agnet {c.get_id} and I'm {c.type}")

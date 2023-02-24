from copy import deepcopy
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
    
    def reconsider(self, pms):
        """"Mechanism that changes agents mind based on given probabilities"""
        choice = ['fundamentalist', 'noise_optimist', 'noise_pessimist']
        delta_t = pms['delta_t']

        if self.type == 'fundamentalist':
            f_plus = delta_t*pms['pi_f_plus'] #probabiliti for fundamentalist to become optimist
            f_minus =delta_t*pms['pi_f_minus'] #probabiliti for fundamentalist to become pessimist
            f_f = 1-f_plus-f_minus #probability for fundamentalist to stay fundamentalist 
            w = [f_f, f_plus, f_minus]
            new_type = choices(choice, w)
            if new_type != ['fundamentalist']:
                self.type = new_type[0]

        elif self.type == 'noise_optimist':
            plus_f = delta_t*pms['pi_plus_f'] 
            plus_minus = delta_t*pms['pi_plus_minus'] 
            plus_plus = 1-plus_f-plus_minus 
            w = [plus_f, plus_plus, plus_minus]
            new_type = choices(choice, w)
            if new_type != ['noise_optimist']:
                self.type = new_type[0]

        elif self.type == 'noise_pessimist':
            minus_f = delta_t*pms['pi_minus_f']
            minus_plus = delta_t*pms['pi_minus_plus'] 
            minus_minus = 1 - minus_f - minus_plus
            w = [minus_f, minus_plus, minus_minus]
            new_type = choices(choice, w)
            if new_type != ['noise_pessimist']:
                self.type = new_type[0]
        return self
        
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

    
#     self.__step_values['pi_plus_minus']= Functions.pi_f_minus(self.__params, dp_dt)
#             self.__step_values['pi_minus_plus']=Functions.pi_minus_plus(self.__params, dp_dt)
#             self.__step_values['pi_plus_f']=Functions.pi_plus_f(self.__params, dp_dt)
#             self.__step_values['pi_f_plus']=Functions.pi_f_plus(self.__params, dp_dt)
#             self.__step_values['pi_minus_f']=Functions.pi_minus_f(self.__params, dp_dt)
#             self.__step_values['pi_f_minus']=Functions.pi_f_minus(self.__params, dp_dt)



#agent = Agent(1)
#print(agent.type)
#agent.type = 'noise_optimist'
#print(agent.type)
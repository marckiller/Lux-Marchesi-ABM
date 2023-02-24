from copy import deepcopy
from Functions import Functions
from Agent import Agent
from LoadConfiguration import Configuration
from random import choices
import numpy as np
import json

class MarketSimulation:

    def __init__(self, params) -> None:

        #We will use seld.__params as parameters and curent values source (some of the values will be changed, others will stay)
        #the idea is that dictonary of params woulb be enough to save almost all informations about silulation (single agents history is not stored but could be by adding seld.__agents field to dict)

        if isinstance(params, Configuration):
            self.__params = params.get_variables()
        elif isinstance(params, dict):
            self.__params = params
        else:
            print('Parameters should be dict!') #dict is used for code simplicity
        
        #reserving slots for transition probabilities. notation as in the paper 
        self.__params['pi_minus_plus'] =0
        self.__params['pi_plus_minus'] =0
        self.__params['pi_plus_f'] =0
        self.__params['pi_f_plus'] =0
        self.__params['pi_minus_f'] =0
        self.__params['pi_f_minus'] =0
        self.__params['pi_price_up']=0
        self.__params['pi_price_down']=0

        #we also store directly info about price change and value change probabilities 
        self.__params['pi_price_up'] =0
        self.__params['pi_price_down'] =0
        #we also store directly info about price change and value change probabilities 
        self.__params['price_change'] =0
        self.__params['value_change'] =0

        #we set counter of market iterations here
        self.__params['iteration'] = 0

        #count total number of gents (that is not directly put into configuration file)
        self.__params['N'] = self.__params['num_fundamentalists'] + self.__params['num_noise_optimist'] + self.__params['num_noise_pessimist'] 
        self.__params['minimal_population+of_given_agent_type'] = self.__params['N']*self.__params['minimal_agent_population_frac']
    
        #W also add dp_dt as parameter
        self.__params['dp_dt'] = 0

        #list of agents in our enviroment
        self.__agents = []

        #we could have created agents in __init__ but I chose not to 
        #self.create_agents 

        self.__history = [deepcopy(self.__params)]

    def create_agents(self):
        """Fill the list of agents"""
        #initialize N agents
        for i in range(self.__params['N']):
            self.__agents.append(Agent(id = i))

        #change n_+ to noise optimists:
        for i in range(self.__params["num_noise_optimist"]):
            self.__agents[i].type = 'noise_optimist'

        #change n_- to noise pessimists: 
        for i in range(self.__params["num_noise_pessimist"]):
            self.__agents[i+self.__params["num_noise_optimist"]].type = 'noise_pessimist'
        
        #History for step 0 is already saved. It's saved during init
        #Show info about initialized market 
        print(f"Market created: total number of traders: {self.__params['N']} \n fundamentalists: {self.__params['num_fundamentalists']} \n noise optimists: {self.__params['num_noise_optimist']} \n noise pessimists: {self.__params['num_noise_pessimist']} \n market price: {self.__params['market_price']} \n market value: {self.__params['market_value']}")

    def step(self):
        #hisotry is already created so we can use it 
        
        #1: timer tick
        self.__params['iteration'] += 1

        #2: Real value changes. We also saevd how did it change
        self.__params['market_value'] = Functions.probablistic_value_change(self.__params)
        self.__params['value_change'] = self.__history[self.__params['iteration'] - 1]['market_value'] - self.__params['market_value']

        #2.1: Price change
        mu = np.random.normal(self.__params['price_change_mu'], self.__params['price_change_sigma'])
        self.__params['pi_price_up'] = Functions.prob_price_increase(self.__params,  mu)
        self.__params['pi_price_down'] =Functions.prob_price_decrease(self.__params,  mu)
        choice = [1,-1]
        weights = [self.__params['pi_price_up'], self.__params['pi_price_down']]
        self.__params['price_change'] = choices(choice, weights)[0]*self.__params['delta_p']*self.__params['market_price']
        self.__params['market_price'] += self.__params['price_change']

        #2.2: expresind dp_dt
        if self.__params['iteration'] < 30:
            self.__params['dp_dt'] = (self.__params['market_price'] - self.__history[0]['market_price'])/self.__params['iteration']
        else:
            self.__params['dp_dt'] = (self.__params['market_price'] - self.__history[self.__params['iteration'] -30]['market_price'])/30
        self.__params['pi_minus_plus'] = Functions.pi_minus_plus(self.__params)
        self.__params['pi_plus_minus'] = Functions.pi_plus_minus(self.__params)
        self.__params['pi_plus_f'] = Functions.pi_plus_f(self.__params)
        self.__params['pi_f_plus'] = Functions.pi_f_plus(self.__params)
        self.__params['pi_minus_f'] = Functions.pi_minus_f(self.__params)
        self.__params['pi_f_minus'] = Functions.pi_f_minus(self.__params)
        
        #4: Agents adjusting their strategies
        delta_f, delta_o, delta_p = 0,0,0    #we will see as an output how agents population changed during simulaiton. We cant change seld.__params['num_fundamentalist] dinamically because it would affect market during
                                             #one step more than once
        for agent in self.__agents:
            i_was = agent.type
            if i_was == 'fundamentalist' and self.__params['minimal_population+of_given_agent_type'] < self.__params['num_fundamentalists']:
                agent.reconsider(self.__params)              
            elif i_was == 'noise_pessimist' and self.__params['minimal_population+of_given_agent_type'] < self.__params['num_noise_pessimist']:
                agent.reconsider(self.__params)
            elif i_was == 'noise_optimist' and self.__params['minimal_population+of_given_agent_type'] < self.__params['num_noise_optimist']:
                agent.reconsider(self.__params)
            i_am = agent.type 

            if i_was != i_am:
                if i_was == 'fundamentalist':
                    delta_f -= 1
                elif i_was == 'noise_pessimist':
                    delta_p -= 1
                elif i_was == 'noise_optimist':
                    delta_o -= 1

                if i_am == 'fundamentalist':
                    delta_f += 1
                elif i_am == 'noise_pessimist':
                    delta_p += 1
                elif i_am== 'noise_optimist':
                    delta_o += 1
        self.__params['num_fundamentalists'] += delta_f
        self.__params['num_noise_optimist'] += delta_p         
        self.__params['num_noise_pessimist'] += delta_o   

        #5: saving history
        self.__history.append(deepcopy(self.__params))     

    def get_history(self):
        return self.__history

    def start_simulation(self):
        for i in range(self.__params['num_of_steps']):
            if i % 200 == 0:
                print(i)
            self.step()

    def save_to_file(self, filename = 'output.txt'):
        with open(filename, 'w') as f:
            json.dump(self.__history, f)



        


        
        




from Agent import Agent
from LoadConfiguration import Configuration
from Decision import Decision
import numpy as np
from Functions import Functions
import matplotlib.pyplot as plt
from random import choices

class Simulation:

    def __init__(self, pms, save_history_to_file = False):
        self.__pms = pms
        self.__number_of_agents = pms['num_fundamentalists'] + pms['num_noise_optimist'] + pms['num_noise_pessimist']
        self.__agents = []
        self.__timer = 0
        self.__history = [[self.__timer, self.__agents, self.__pms['market_value'], self.__pms['market_price']]]
    
    def create_agents(self):
        for i in range( self.__number_of_agents):
            self.__agents.append(Agent(id = i))
        for i in range(self.__pms['num_noise_optimist']):
            self.__agents[i+self.__pms['num_fundamentalists']].type = 'noise_optimist'
        for i in range(self.__pms['num_noise_pessimist']):
            self.__agents[i+self.__pms['num_noise_optimist']+self.__pms['num_fundamentalists']].type = 'noise_pessimist'
    
    def agents_say_hello(self):
        for i in self.__agents:
            print(i)

    def step(self):
        #timer += 1
        self.__timer += 1

        #market_value change changed. We will recive value from previous step from self.__history
        self.__pms['market_value'] = Functions.prob_value_change(self.__pms)

        #now we check how price changed. To do it we'll use Functions package. for now we need only parameters
        #######change = self.__pms['market_value']-(self.__history[self.__timer-1][2])
        
        m_u = np.random.normal(loc=0, scale=0.02)
        p_price_up, p_price_down = Functions.prob_price_increase(self.__pms, m_u), Functions.prob_price_decrease(self.__pms, m_u)
        weights = [p_price_up, p_price_down]
        choice = [0.001*self.__pms['market_price'], -0.001*self.__pms['market_price']]
        self.__pms['market_price'] += choices(choice, weights)[0]

        #now we can see how price changed (and divide it by curen price p)
        if self.__timer > 30:
            dp_dt = (self.__pms['market_price'] - self.__history[self.__timer-30][3])*(1/self.__pms['market_price'])
        else:
            dp_dt = (self.__pms['market_price'] - self.__history[self.__timer-1][3])*(1/self.__pms['market_price'])

        #now we can count probabilities of changing adequate states. We have to remember about correct correct sequence
        # 0: opt -> pes
        # 1: pes -> opt
        # 2: opt -> fund
        # 3: pes -> fund
        # 4: fund -> opt
        # 5: fund -> pes 
        prob = [Functions.pi_plus_minus(self.__pms, dp_dt),
                Functions.pi_minus_plus(self.__pms, dp_dt),
                Functions.pi_plus_f(self.__pms, dp_dt),
                Functions.pi_minus_f(self.__pms, dp_dt),
                Functions.pi_f_plus(self.__pms, dp_dt),
                Functions.pi_f_minus(self.__pms, dp_dt)]
        for agents in self.__agents:
            agents.rethink_strategy(prob)

        self.__history.append([self.__timer, self.__agents, self.__pms['market_value'], self.__pms['market_price']])
    
    def get_history(self):
        return self.__history
            
config = Configuration()
var = config.get_variables()
print(var)

sim = Simulation(pms = var)
sim.create_agents()
sim.agents_say_hello()

for _ in range(1000):
    sim.step()

history = sim.get_history()
print(history[1][2])
print(history[2][2])
price_hist = []
val_his = []
for i in range(len(history)):
    price_hist.append(history[i][3])
    val_his.append(history[i][2])
plt.plot(price_hist)
plt.plot(val_his)
plt.show()

#plt.plot(pices)
#plt.show()


#test = []
#for i in range(10000):
#    a = Functions.prob_value_change(var)
#    test.append(Functions.prob_value_change(var))
#    var['market_value'] = a
#print(test) 
#
#
## Example list of values
#values = [1, 3, 5, 4, 6, 8]
#
## Create the plot
#plt.plot(test)
#plt.show()
#
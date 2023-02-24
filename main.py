from copy import deepcopy
from Functions import Functions
from Agent import Agent
from LoadConfiguration import Configuration
from MarketSimulation import MarketSimulation
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd 
import math
import Extraction_lib
import os
from datetime import datetime
import shutil
import json

def plot_agents():
    plt.clf()
    plt.plot(num_fundamentalists, label='num_fundamentalists')
    plt.plot(num_noise_optimist, label='num_noise_optimist')
    plt.plot(num_noise_pessimist, label='num_noise_pessimist')
    plt.legend()
    plt.gcf().set_dpi(300)
    plt.gcf().set_size_inches(15, 6)
    plt.savefig('agents.png', dpi=300, bbox_inches='tight')
    shutil.move("agents.png", f"{timestamp}/agents.png")
    
def plot_prices():
    plt.clf()
    plt.plot(market_price, label='market_price')
    plt.plot(market_value, label='market_value')
    plt.legend()
    plt.gcf().set_dpi(300)
    plt.gcf().set_size_inches(15, 6)
    plt.savefig('prices.png', dpi=300, bbox_inches='tight')
    shutil.move("prices.png", f"{timestamp}/prices.png")

def plot_pi():
    plt.clf()
    plt.plot(pi_minus_plus, label='pi_minus_plus')
    plt.plot(pi_plus_minus, label='pi_plus_minus')
    plt.plot(pi_plus_f, label='pi_plus_f')
    plt.plot(pi_f_plus, label='pi_f_plus')
    plt.plot(pi_minus_f, label='pi_minus_f')
    plt.plot(pi_f_minus, label='pi_f_minus')
    plt.legend()
    plt.gcf().set_dpi(300)
    plt.gcf().set_size_inches(15, 6)
    plt.savefig('pi_values.png', dpi=300, bbox_inches='tight')
    shutil.move("pi_values.png", f"{timestamp}/pi_values.png")


def plot_price_tick_prob():
    plt.clf()
    plt.plot(pi_price_up, label='pi_price_up')
    plt.plot(pi_price_down, label='pi_price_down')
    plt.legend()
    plt.show()
    
def plot_price_change():
    plt.clf()
    plt.plot(price_change, label='price_change')
    plt.plot(value_change, label='value_change')
    plt.legend()
    plt.show()

def plot_dp_dt():
    plt.clf()
    plt.plot(dp_dt, label='dp_dt')
    plt.legend()
    plt.show()

def save_initial_configuration():
    initial_values = history[0]
    filename = 'input.txt'
    with open("input.txt", "w") as f:
        for key, value in initial_values.items():
            f.write(f"{key}: {value}\n")
        shutil.move("input.txt", f"{timestamp}/input.txt")



####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

#reading configuraiton from json
config = Configuration()

#creating market
simul = MarketSimulation(config)

#creating traders
simul.create_agents()

#running simulation
simul.start_simulation()

#get hitory
hisotry = simul.get_history()

#saving history to file
simul.save_to_file()

#creating folder
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
os.mkdir(timestamp)

#keys that we will use to create plots
keys=['num_fundamentalists','num_noise_optimist','num_noise_pessimist',
    'market_price',
    'market_value',
    'pi_minus_plus', 'pi_plus_minus', 'pi_plus_f', 'pi_f_plus', 'pi_minus_f', 'pi_f_minus', 
    'pi_price_up', 'pi_price_down', 
    'price_change', 'value_change',
    'dp_dt']

#extracting history file
history = Extraction_lib.read_history()
shutil.move("output.txt", f"{timestamp}/output.txt")

#creation of variables
for elements in keys:
    globals()[elements] = Extraction_lib.read_variable(history, elements)

#creating plots and saving initial configuration to dedicated folder
plot_agents()
plot_pi()
plot_prices()
save_initial_configuration()

    





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
import csv

def plot_agents():
    plt.clf()
    plt.plot(num_fundamentalists, label='fundamentalists')
    plt.plot(num_noise_optimist, label='noise optimists')
    plt.plot(num_noise_pessimist, label='noise pessimists')
    plt.legend()
    plt.gcf().set_dpi(300)
    plt.gcf().set_size_inches(15, 6)
    plt.savefig('agents.png', dpi=300, bbox_inches='tight')
    shutil.move("agents.png", f"{timestamp}/agents.png")
    
def plot_prices():
    plt.clf()
    plt.plot(market_price, label='market price')
    plt.plot(market_value, label='real value')
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

def plot_value_cahnges():
    #'relative_change_of_fundamental_value','relative_change_of_price']
    plt.clf()
    plt.plot(rch1, label = 'tau = 1')
    plt.plot(rch5, label = 'tau = 5')
    plt.plot(rch15, label = 'tau = 15')
    plt.plot(rch25, label = 'tau = 25')
    plt.legend()
    plt.loglog()
    plt.gcf().set_dpi(300)
    plt.gcf().set_size_inches(15, 6)
    plt.savefig('relative_value_change.png', dpi=300, bbox_inches='tight')
    shutil.move("relative_value_change.png", f"{timestamp}/relative_value_change.png")


def plot_price_changes():
    plt.clf()
    plt.plot(pch1, label = 'tau = 1')
    plt.plot(pch5, label = 'tau = 5')
    plt.plot(pch15, label = 'tau = 15')
    plt.plot(pch25, label = 'tau = 25')
    plt.legend()
    plt.loglog()
    plt.gcf().set_dpi(300)
    plt.gcf().set_size_inches(15, 6)
    plt.savefig('relative_price_change.png', dpi=300, bbox_inches='tight')
    shutil.move("relative_price_change.png", f"{timestamp}/relative_price_change.png")


def save_value_price():
    with open('value_vs_price.csv', 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)
        # Write the two lists as rows in the CSV file
        writer.writerow(market_value)
        writer.writerow(market_price)
        shutil.move("value_vs_price.csv", f"{timestamp}/value_vs_price.csv")



#def plot_returns_tau():
#    pass



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

def plot_price_and_value_changes():
    plt.clf()
    plt.plot(changes_of_market_price, label='market price')
    plt.legend()
    plt.gcf().set_dpi(300)
    plt.gcf().set_size_inches(15, 6)
    plt.savefig('relative_changes_of_market_price.png', dpi=300, bbox_inches='tight')
    shutil.move("relative_changes_of_market_price.png", f"{timestamp}/relative_changes_of_market_price.png")

    plt.clf()
    plt.plot(changes_of_fundamental_value, label='fundamental value')
    plt.legend()
    plt.gcf().set_dpi(300)
    plt.gcf().set_size_inches(15, 6)
    plt.savefig('relative_changes_of_fundamental_value.png', dpi=300, bbox_inches='tight')
    shutil.move("relative_changes_of_fundamental_value.png", f"{timestamp}/relative_changes_of_fundamental_value.png")

    plt.clf()
    plt.plot(changes_of_fundamental_value, label='fundamental value')
    plt.plot(changes_of_market_price, label='market price')
    plt.legend()
    plt.gcf().set_dpi(300)
    plt.gcf().set_size_inches(15, 6)
    plt.savefig('relative_changes_of_fundamental_value_and_price.png', dpi=300, bbox_inches='tight')
    shutil.move("relative_changes_of_fundamental_value_and_price.png", f"{timestamp}/relative_changes_of_fundamental_value_and_price.png")


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
    #,'relative_change_of_fundamental_value','relative_change_of_price']

#extracting history file
history = Extraction_lib.read_history()
shutil.move("output.txt", f"{timestamp}/output.txt")

#creation of variables
for elements in keys:
    globals()[elements] = Extraction_lib.read_variable(history, elements)
#print(market_value)

precision = 0.002
one = int(1/precision)

#Recreating plots from paper
changes_of_market_price =[]
changes_of_fundamental_value = []
for i in range(len(market_value)-one):
    changes_of_market_price.append(math.log(market_price[i+one])-math.log(market_price[i]))
    changes_of_fundamental_value.append(math.log(market_value[i+one])-math.log((market_value[i])))

#creating plots and saving initial configuration to dedicated folder
plot_agents()
plot_pi()
plot_prices()
save_initial_configuration()
save_value_price()
plot_price_and_value_changes()








import os
import datetime
import json
import csv
from matplotlib import pyplot as plt

def read_variable(history, name):
    var = []
    for i in range(len(history)):
        var.append(history[i][name])
    return var

def read_history(name = 'output.txt'):
    with open(name, 'r') as f:
        list_of_dicts = json.load(f)
    return list_of_dicts

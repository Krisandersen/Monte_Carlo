
'''This is an example code for a Monte Carlo Simulation. If you see any improvements (Which I have no doubt that there might be) then let me know'''

import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.stats import norm
from tqdm import tqdm
import statistics
from pandas import DataFrame
from tqdm import tqdm_gui
import time
import pylab


#input values for simulation
companyname = input("What is the name of the company you are wanting to simulate? ")
ticker = input(f"What is the ticker of {companyname}? ")
t_intervals = int(input("How many days do you want the simulation to simulate? "))
iterations = int(input("How many iterations would you like to do? "))
timeframe = input("What year would you like as base year for volatility calculations? ")
saveornot = input("Do you want to save it(s), present it(p), or both(b)? ").lower()




def get_simulation(ticker, name, t_intervals, iterations, saveornot, timeframe):
    data = pd.DataFrame()
    data[ticker] = wb.DataReader(ticker, data_source='yahoo', start=timeframe)['Adj Close']


    log_returns = np.log(1 + data.pct_change())
    u = log_returns.mean()

	# Essentially this is how far stock prices are spread out from the mean
    var = log_returns.var()

	# This is the change the average value in our stock prices over time.
    drift = u - (0.5 * var)

	# This is a measure of the dispersion of the stock prices. 
    stdev = log_returns.std()

    #Here we find the daily returns and add then to our dataframe
    daily_returns = np.exp(drift.values + stdev.values * norm.ppf(np.random.rand(t_intervals, iterations)))
    S0 = data.iloc[-1]
	

	# Here we are using np.zeros_like to create a numpy array, which is filled with zeros but has the same shape as the daily_returns numpy array. 
    price_list = np.zeros_like(daily_returns)
    price_list[0] = S0


    pbar = tqdm(total=100)
    pbar_increments = 100/t_intervals
    for t in tqdm(range(1, t_intervals)):
        price_list[t] = price_list[t - 1] * daily_returns[t]
        time.sleep(0.01)


    print("Just hold on. Making the Monte Carlo plot can takes some time")

    expectedx = round(np.mean(price_list[-1]),4)
    
    mpl.use('TkAgg')

    # The next few lines are a plot made with matplotlib.
    plt.figure(figsize=(10,6))
    #Below is the code to set the title of the plot. Name is derived from the input of the function
    plt.title(f"{t_intervals} days Monte Carlo Simulation for " + name + ". E(x) = " + str(expectedx))
    #The next two lines are the x and y label
    plt.ylabel("Price (P)")
    plt.xlabel("Time (Days)")
    #This is the line of code that actually plots every single list that we have
    plt.plot(price_list);
    #The line below is commented out by default. If you want to include it comment out the line /n
    #below it as they are best used separately to save some computing time. 
    # Especially with higher number of iterations!!
    
    if saveornot == "s":
        plt.savefig(f"{companyname} Monte Carlo Simulation")
    elif saveornot =="p":
        plt.show()
    else:
        plt.savefig(f"{companyname} Monte Carlo Simulation")
        plt.show()

get_simulation(ticker, companyname, t_intervals, iterations, saveornot, timeframe)

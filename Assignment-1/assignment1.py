import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import norm
from scipy.special import binom

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--p", help="The probability with which a ball goes to the right.")
parser.add_argument("--N", help="The number of balls.")
parser.add_argument("--n", help="The dimension of the board.")
parser.add_argument("--binomial", help="To print and calculate the binomial approximation.", action="store_true")
parser.add_argument("--gaussian", help="To print and calculate the gaussian approximation.", action="store_true")

args=parser.parse_args()

# Taking N = number of balls
if(args.N and int(args.N) > 0):
    N = int(args.N)   
else:
    N = 500

# Taking n = dimension of the board
if(args.n and int(args.n) > 0):
    n = int(args.n)     
else:
    n = 50

# Taking p = probability of going to the right
if(args.p and float(args.p) > 0 and float(args.p) <= 1):
    p = float(args.p)
else:
    p = 0.5

# Simulating the movement of the balls.
# bag is the final vector that contains, for each cell, the number of balls fallen into it.
bag = [0 for i in range(n)]
for i in range(1, N):
    position = [0, 0]
    for k in range(1, n):
        position[random.choices([0,1], [1-p, p])[0]] += 1
    bag[position[1]] += 1

# x contains the numbers from 0 to n-1 that indicate the n final cells.
x = np.arange(len(bag))
bag = np.array(bag)
normalizedBag = np.divide(bag, N)

figure, graph = plt.subplots()
graph.bar(x, normalizedBag, label="Data", color="y")

###################### BINOMIAL APPROXIMATION using p
if(args.binomial):
    binPoints = []
    for i in x:
        binPoints.append(binom(n, i)*(p**i)*((1-p)**(n-i)))
    graph.bar(x, binPoints, 0.2, label="Binomial approximation", color="b")

    # MSE between binomial and points
    MSE_bin_points = 0
    for i in range(0, len(x)):
        MSE_bin_points = MSE_bin_points + (binPoints[i] - normalizedBag[i])**2
    print("MSE_bin_points = " + str(MSE_bin_points))

##################### GAUSSIAN APPROXIMATION with binomial
if(args.gaussian):
    def gaussianFunc(x, mu, sigma):
        return (1/(sigma*np.sqrt(2*np.pi)))*np.exp(-(x-mu)**2/(2*sigma**2))

    popt, pcov = curve_fit(gaussianFunc, x, binPoints, bounds=((0,np.inf)))
    plt.plot(x, gaussianFunc(x, *popt), 'r-', label='Gaussian approximation')

    print("Estimated gaussian parameters: mu = " + str(popt[0]) + ", sigma = " + str(popt[1]))
 
    # MSE between binomial and gaussian approximation
    if(args.binomial):
        MSE_bin_gauss = 0
        for i in range(0, len(x)):
            MSE_bin_gauss = MSE_bin_gauss + (binPoints[i] - gaussianFunc(i, *popt))**2
        print("MSE_bin_gauss = " + str(MSE_bin_gauss))

# Adding an additional scale on the y-axis to see the original values of the number of balls fallen into the cells
y2 = graph.twinx()
y2.set_ylim([0, graph.get_ylim()[1] * N])
y2.set_ylabel('Number of balls')

# Plotting the graph
graph.set_ylabel('Number of balls / N')
graph.set_xlabel('Cell')
figure.tight_layout()
graph.legend()

plt.show()
import randomhash
import argparse
import math
import numpy as np
import scipy

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

parser = argparse.ArgumentParser()

parser.add_argument("--data", help="The file with the data to be used (each line should be an entry).", required=True)
parser.add_argument("--T", help="Number of times the algorithm is run for the prediction.", default=300, type=check_positive)
parser.add_argument("--m", help="Parameter m.", default=256, type=check_positive)
parser.add_argument("--model", help="The model to be used for estimating delta.", default=1, type=int, choices=[1,2,3])
parser.add_argument("--realCardinality", help="If set, the real cardinality will be used to estimate delta; otherwise, the experiment will be run with the chosen model.", type=check_positive)

args = parser.parse_args()
T = args.T

#################### ALGORITHMS
def countZeroes(binaryString):
    counter = 0
    for i in binaryString:
        if i == '1':
            break
        counter += 1
    return counter

# memory: as HLL
def Experimenting(file, delta, m):
    rfh = randomhash.RandomHashFamily()
    R = [0 for i in range(m)]
    sign = int(math.log2(m))
    for word in file.readlines():
        digest = bin(rfh.hash(word.rstrip("\n")))[2:][::-1]
        substream = int(digest[0:sign], 2)
        current = countZeroes(digest[sign:]) + 1
        if current > R[substream]:
            R[substream] = current

    if delta != False:
        return delta * m * 2**(m/sum(1/R[i] for i in range(m) if R[i] != 0))
    return args.realCardinality/(m * 2**(m/sum(1/R[i] for i in range(m) if R[i] != 0)))

def model1(m):
    a = 0.000273
    b = 0.2401
    c = 0.5036
    return a*math.gamma(1/m) + b*1/m + c

def model2(m):
    a = 13.845
    b = 1.598
    c = -11.773
    return a * math.gamma(-1/m + b) + c

def model3(m):
    a = 0.000242
    b = 0.782
    c = 0.503
    return a * scipy.integrate.quad(lambda u: np.log(b*u+m), 0, np.inf)[0] + c
    


if __name__ == "__main__":
    try:
        file = open(args.data, "r")
    except:
        print("File not found, please try again.")
        exit()

    if args.realCardinality:
        delta_s = []
        print("-------- Estimating delta with " + str(T) + " rounds, m = " + str(args.m) + ". --------")
        m = args.m
        for t in range(T):
            delta = Experimenting(file, False, m)
            # print("-- Iteration " + str(t) + ": delta = " + str(delta))
            delta_s.append(delta)
            file.seek(0)

        print("Estimated value of delta after " + str(T) + " rounds = " + str(np.mean(delta_s)) + ", emp. std. dev = " + str(np.std(delta_s, ddof = 1)) + ".")

    else:
        Z_s = []
        print("-------- Estimating cardinality with " + str(T) + " rounds, m = " + str(args.m) + ". --------")
        m = args.m
        if args.model == 1:
            delta = model1(m)
        elif args.model == 2:
            delta = model2(m)
        else:
            delta = model3(m)
        print("Delta = " + str(delta))
        for t in range(T):
            Z = Experimenting(file, delta, m)
            # print("-- Iteration " + str(t) + ": delta = " + str(delta))
            Z_s.append(Z)
            file.seek(0)

        print("Estimated value of cardinality after " + str(T) + " rounds = " + str(np.mean(Z_s)) + ", emp. std. dev = " + str(np.std(Z_s, ddof = 1)) + ".")
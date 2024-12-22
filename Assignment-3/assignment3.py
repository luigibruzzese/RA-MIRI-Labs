import randomhash
import argparse
import math
import scipy.integrate
from sortedcontainers import SortedList
import scipy
import numpy as np

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

parser = argparse.ArgumentParser()
parser.add_argument("--data", help="The file with the data to be used (each line should be an entry).", required=True)
parser.add_argument("--alg", help="The algorithm to be used, either HyperLogLog (HLL), Recordinality (REC), LogLog (LL) or Adaptive Sampling (AS).", choices=["HLL", "REC", "LL", "AS"], required=True)
parser.add_argument("--T", help="Number of times the algorithm is run for the prediction.", default=1000, type=check_positive)
parser.add_argument("--param", help="Parameter m for LL and HLL; k for REC; maxS for AS.", default=256, type=check_positive)

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

# HLL: SE = 1.03/sqrt(m)
# memory: as LL
def HyperLogLog(file, alfa, m):
    rfh = randomhash.RandomHashFamily()
    R = [0 for i in range(m)]
    sign = int(math.log2(m))
    for word in file.readlines():
        digest = bin(rfh.hash(word.rstrip("\n")))[2:][::-1]
        substream = int(digest[0:sign], 2)
        current = countZeroes(digest[sign:]) + 1
        if current > R[substream]:
            R[substream] = current

    return alfa * m**2 * sum(2**(-R[i]) for i in range(m))**(-1)

# Log log: SE = 1.3/sqrt(m)
# memory: m*loglog(n/m)
def LogLog(file, alfa, m):
    rfh = randomhash.RandomHashFamily()
    R = [0 for i in range(m)]
    sign = int(math.log2(m))
    for word in file.readlines():
        digest = bin(rfh.hash(word.rstrip("\n")))[2:][::-1]
        substream = int(digest[0:sign], 2)
        current = countZeroes(digest[sign:]) + 1
        if current > R[substream]:
            R[substream] = current

    return alfa * m * 2**(sum(R[i] for i in range(m))/m)




# memory: klogn (hash values in S) + loglogn (the counter R)
# accuracy = sqrt((n/(ke))^1/k - 1)
def Recordinality(file):
    rfh = randomhash.RandomHashFamily()
    k = args.param
    R = 0
    S = SortedList()
    while R < k:              # complexity: O(k*logK)
        word = file.readline()
        digest = bin(rfh.hash(word.rstrip("\n")))[2:][::-1]
        # digest = word.rstrip("\n")
        if not(digest in S):
            S.add(digest)
            R += 1
    for word in file.readlines():
        digest = bin(rfh.hash(word.rstrip("\n")))[2:][::-1]
        # digest = word.rstrip("\n")
        if digest > S[0] and not(digest in S):          # complexity 1 + O(logn)
            S.add(digest)           # complexity O(logn)
            S.pop(0)                # complexity O(logn)
            R += 1
    return k*(1+1/k)**(R-k+1) - 1

# accuracy: 1.20/sqrt(m)
# bounded by maxS!
# memory: maxS*logn (hash values in S) + loglogn (the depth p)
def AdaptiveSampling(file):
    rfh = randomhash.RandomHashFamily()
    maxS = args.param
    S = []
    p = 0
    for word in file.readlines():
        digest = bin(rfh.hash(word.rstrip("\n")))[2:][::-1]
        if countZeroes(digest) >= p and not(digest in S):
            S.append(digest)
            if len(S) > maxS:
                p += 1
                S[:] = [x for x in S if countZeroes(x) >= p]
    return 2**p * len(S)
    

if __name__ == "__main__":
    try:
        file = open(args.data, "r")
    except:
        print("File not found, please try again.")
        exit()

    Z_s = []
    if args.alg == "HLL":
        print("-------- CONFIGURATION selected: algorithm HyperLogLog, " + str(T) + " rounds, m = " + str(args.param) + ". --------")
        # Calculating alfa to do it only once (it depends on m)
        m = args.param
        alfa = (m * scipy.integrate.quad(lambda u: (np.log2((2+u)/(1+u)))**m, 0, np.inf)[0])**(-1)
        for t in range(T):
            Z = HyperLogLog(file, alfa, m)
            # print("-- Iteration " + str(t) + ": Z = " + str(Z))
            Z_s.append(Z)
            file.seek(0)
    elif args.alg == "LL":
        print("-------- CONFIGURATION selected: algorithm LogLog, " + str(T) + " rounds, m = " + str(args.param) + ". --------")
        # Calculating alfa to do it only once (it depends on m)
        m = args.param
        alfa = (math.gamma(-1/m) * (1-2**(1/m)) / math.log(2)) ** (-m)
        for t in range(T):
            Z = LogLog(file, alfa, m)
            # print("-- Iteration " + str(t) + ": Z = " + str(Z))
            Z_s.append(Z)
            file.seek(0)
    elif args.alg == "AS":
        print("-------- CONFIGURATION selected: algorithm Adaptive Sampling, " + str(T) + " rounds, m = " + str(args.param) + ". --------")
        for t in range(T):
            Z = AdaptiveSampling(file)
            # print("-- Iteration " + str(t) + ": Z = " + str(Z))
            Z_s.append(Z)
            file.seek(0)
    elif args.alg == "REC":
        print("-------- CONFIGURATION selected: algorithm Recordinality, " + str(T) + " rounds, k = " + str(args.param) + ". --------")
        for t in range(T):
            Z = Recordinality(file)
            # print("-- Iteration " + str(t) + ": Z = " + str(Z))
            Z_s.append(Z)
            file.seek(0)

    print("Estimated value of Z after " + str(T) + " rounds = " + str(np.mean(Z_s)) + ", emp. std. dev = " + str(np.std(Z_s, ddof = 1)) + ".")
    # print("Estimated value of Z = " + str(np.mean(Z_s)))
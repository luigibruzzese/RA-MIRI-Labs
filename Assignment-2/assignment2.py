import argparse
import matplotlib.pyplot as plt
import random
import numpy

parser = argparse.ArgumentParser()

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

def check_probability(value):
    ivalue = float(value)
    if ivalue < 0 or ivalue > 1:
        raise argparse.ArgumentTypeError("%s is an invalid probability value" % value)
    return ivalue

parser.add_argument("--n", help="The number of balls (default = 100).", default=100, type=check_positive)
parser.add_argument("--m", help="The number of bins (default = 20).", default=20, type=check_positive)
parser.add_argument("--T", help="The number of rounds for calculating the average gap (default = 10).", default=10, type=check_positive)
parser.add_argument("--d", help="The number of choices for the d-choices strategy (default = 1).", default=1, type=check_positive)
parser.add_argument("--beta", help="The probability for using one-choice, instead of two-choices, in (1+beta)-choice strategy. If specified, d is ignored. Default = unset.", type=check_probability)
parser.add_argument("--b", help="The dimension of batch for the b-batched strategy (defaul = 1, i.e., no-batched).", default=1, type=check_positive)
parser.add_argument("--k", help="The number of questions to be asked (either 1 or 2), using the strategy with partial information.", default=0, type=int, choices=[1,2])
parser.add_argument("--analysisStep", help="If set, an analysis on how the gap goes is made starting from n = m (if a different m is specified, it's ignored) to n = m^2, with the specified step.", type=check_positive)

args=parser.parse_args()

m = int(args.m)
n = int(args.n)
T = int(args.T)
d = int(args.d)
b = int(args.b)

# Useful functions for "asking questions" to the bins in the case of partial information

# Returns a string that indicates if the values returned are above or below
def question1 (dRandomBins, x):
    median = numpy.median(x)
    belowMedian = [bin for bin in dRandomBins if x[bin] <= median]
    return belowMedian

def whichBinIsNotInMostLoaded (percentage, dRandomBins, x):
    # Sorting the vector in descending order
    sortedVector = numpy.sort(x)[::-1]
    mostPercentageLoads = sortedVector[: round(percentage*len(x))]
    mostPercentageLoaded = [bin for bin in dRandomBins if x[bin] in mostPercentageLoads]
    if (len(mostPercentageLoaded) == 0 or len(mostPercentageLoaded) == len(dRandomBins)):
        return random.choice(dRandomBins)
    return random.choice([bin for bin in dRandomBins if bin not in mostPercentageLoaded])

if args.analysisStep:
    m = n
    figure, graph = plt.subplots()
    graph.set_title('From ' + str(n) + ' to ' + str(n**2) + ' balls with step ' + str(args.analysisStep))

analysis = True

while(analysis):
    print("----------------")
    print("CONFIGURATION: " + str(n) + " balls, " + str(m) + " bins, " + str(T) + " rounds.")
    print("Average load (n/m) = " + str(n/m))
    if args.beta and args.beta >= 0:
        print("(1 + beta)-choice activated, with beta = " + str(args.beta))
    else:
        print("Strategy: " + str(d) + "-choice.")
    if args.k and d != 1:
        print("Partial information strategy activated, k = " + str(args.k))
    if int(args.b) > 1:
        print("B-batched strategy activated with b = " + str(b))

    print("----------------")

    # Main cycle to repeat the experiment T times
    averageGap = 0
    for t in range(1, T+1):
        # The vector that indicates the load of each bin, from bin 0 to the (m-1)-th
        x = [0 for i in range(m)]

        # Throwing the n balls
        i = 0
        while i < n:
            # Using the b-batched setting (default b = 1, i.e., no-batching)
            x_old = x.copy()
            for _ in range(b):
                if i == n: 
                    break
                # print("Batch " + str(_))
                i += 1

                # (1+beta)-strategy
                if args.beta and args.beta >= 0:
                    d = numpy.random.choice([1, 2], p = [float(args.beta), 1-float(args.beta)])

                dRandomBins = random.sample(range(0, m), d)

                if d > 1 and args.k > 0:
                    answer1 = question1(dRandomBins, x_old)
                    if len(answer1) >= 1:
                        # There are some bins below the median
                        if len(answer1) == 1:
                            selectedBin = answer1[0]
                            # print("Question 1 answer OK: " + str(selectedBin) + " is one of the bins below the median.")
                        elif args.k == 1:
                            # Picking one at random from the one below the median, we can't ask question 2
                            selectedBin = random.choice(answer1)
                            # print("Question 1 didn't help: picked random bin " + str(selectedBin))
                        else:
                            # Asking question 2, to see if one of them is among the 75% most loaded
                            # else pick at random
                            selectedBin = whichBinIsNotInMostLoaded(0.75, dRandomBins, x_old)
                    else:
                        # All the bins are above the median
                        if args.k == 1:
                            # Picking one at random, we can't ask question 2
                            selectedBin = random.choice(dRandomBins)
                            # print("Question 1 didn't help: picked random bin " + str(selectedBin))
                        else:
                            # Asking question 2, to see if one of them is among the 25% most loaded
                            # else pick at random
                            selectedBin = whichBinIsNotInMostLoaded(0.25, dRandomBins, x_old)
                    
                else:
                    # default strategy selecting the bin with the smallest load (or random if there are ties)
                    minLoad = min([x_old[p] for p in dRandomBins])
                    selectedBin = random.choice([p for p in dRandomBins if x_old[p] == minLoad])
                x[selectedBin] += 1

        # print("Round " + str(t) + ": loads of the bins = " + str(x))

        x = [i-n/m for i in x]
        # print("Max-gap = " + str(max(x)))
        averageGap = averageGap + max(x)
    averageGap = averageGap / T
    print("Average gap after " + str(T) + " rounds = " + str(averageGap))

    if args.analysisStep:
        plt.scatter(n, averageGap)
        # plt.annotate(averageGap, (n, averageGap))
        n = n + int(args.analysisStep)
        if n >= m**2:
            analysis = False
    else:
        analysis = False


if args.analysisStep:
    graph.set_ylabel('Average gap')
    graph.set_xlabel('Number of balls')

    ############### For the bounds, uncomment the first row and the one you want to show
    # x_values = [x for x in range(m, n, int(args.analysisStep))]

    # def RS98(n, m):
    #     return numpy.sqrt(n*numpy.log(m)/m)
    # def withD(n, m):
    #     const = 0.9
    #     return numpy.log10(numpy.log10(m))/numpy.log10(int(args.d)) + const

    # d-choice
    # plt.plot(x_values, [RS98(x,m) for x in x_values ], '--r', label="RS98")           # RS-98 for d = 1, with n >> m
    # plt.plot(x_values, [withD(x,m) for x in x_values], '--r')                         # Similar bound with d > 1
   
    # 1+beta
    # plt.plot(x_values, [numpy.log10(m)/(1-float(args.beta)) for i in range(len(x_values))])       # PTW15
    
    # b.batched
    # plt.plot(x_values, [b/m for i in range(len(x_values))])           # d = 2, LS22C
    # plt.plot(x_values, [numpy.sqrt(b*numpy.log10(m)/m) for i in range(len(x_values))])    # using beta, LS22C


    # k questions
    # plt.plot(x_values, [numpy.sqrt(numpy.log10(m)) for i in range(len(x_values))])

    # plt.plot(x_values, [numpy.sqrt(numpy.log10(m)/numpy.log10(numpy.log10(m))) for i in range(len(x_values))])
    # plt.plot(x_values, [int(args.k)*numpy.log10(m**(1/int(args.k))) for i in range(len(x_values))])

    plt.show()

# Gon81
# plt.scatter(n, averageGap)
# plt.scatter(n, numpy.log10(n)/numpy.log10(numpy.log10(n)), marker='x')
# plt.show()
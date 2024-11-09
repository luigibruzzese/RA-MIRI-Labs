UPC - Randomized Algorithms course - A.Y. 2024/2025

## Assignment #2: balanced allocations

This repository contains all the materials delivered for the second assignment in the scope of the Randomized Algorithms course at UPC.
In particular:
- [luigi.bruzzese-balancedalloc.pdf](https://github.com/luigibruzzese/RA-MIRI-Labs/blob/main/Assignment-2/luigi.bruzzese-balancedalloc.pdf) is a report that explains the whole process for fulfilling the assignment;
- [assignment2.py](https://github.com/luigibruzzese/UPC-RA-MIRI-Lab/blob/main/Assignment-2/assignment2.py) is the script used to show the results explained in the report.

The script can be run from a terminal with the following instruction:
  python3 assignment2.py [--n N] [--m M] [--T T] [--d D] [--beta BETA] [--b B] [--k {1,2}] [--analysisStep ANALYSISSTEP]
where the strings enclosed in square brackets are optional and can be used for different purposes. In particular:
- --n=positive integer: sets the integer value of the number of balls N. If not provided, the default value is 100;
- --m=positive integer: sets the number of bins. If not provided, the default value is 20;
- --T=positive integer: sets the number of rounds, i.e., the number of times in which the script has to throw n balls into m bins, in order to calculate the average gap after T rounds. The default value is 10;
- --d=positive integer: sets the number of choices for the d-choices strategies. The default value is 1 (i.e., no choices);
- --beta=float in [0,1]: sets the probability of selecting 1-choices vs 2-choices in the (1+beta)-choices strategy. If set, the value of d is ignored. There's no default value if not specified;
- --b=positive integer: sets the b parameter for the b-batched setting. Default value is 1 (i.e., no batching);
- --k={1,2}: sets the k parameter for the strategy with "questions", i.e., the max. number of questions we can "ask" to bins. Notice that it's not enough to set only k, but d must be > 1, otherwise this strategy makes no sense.
- --analysisStep=positive integer: if specified, the script uses the provided number of balls (n) and, fixing the number of bins m = n, performs a run (i.e., calculates the average gap for T rounds) for each value of n starting from the value provided until n = n^2 (i.e., n = m^2, since m remains the same). The number provided is the step, i.e., the gap on n between two consecutive runs (n(i+1) = n(i) + step). After the computation, the script also prints a plot in which there are the values of n used on the x-axis and, on the y-axis, the corresponding values found for the average gap after the computation.

Notice that the version that has been used is python3.11. Different versions can require further installations of libraries (such as matplotlib, random) that are used in the script to achieve the provided results.

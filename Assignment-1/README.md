UPC - Randomized Algorithms course - A.Y. 2024/2025

## Assignment #1: simulation of a Galton board

This repository contains all the materials delivered for the first assignment in the scope of the Randomized Algorithms course at UPC.
In particular:
- [Bruzzese_Luigi-galtonbox.pdf](https://github.com/luigibruzzese/RA-MIRI-Labs/blob/7f13e9cc5eeba2620d500370810d8bc02638ff1d/Assignment-1/Bruzzese_Luigi-galtonbox.pdf) is a report that explains the whole process for fulfilling the assignment;
- [assignment1.py](https://github.com/luigibruzzese/RA-MIRI-Labs/blob/7f13e9cc5eeba2620d500370810d8bc02638ff1d/Assignment-1/assignment1.py) is the script used to show the results explained in the report;
- [img](https://github.com/luigibruzzese/RA-MIRI-Labs/blob/7f13e9cc5eeba2620d500370810d8bc02638ff1d/Assignment-1/img) is a directory that contains the images used in the report (following the same notation), that can be used to see the provided results in a bigger window.

The script can be run from a terminal with the following instruction:
  python3 assignment1.py [--N=integer] [--n=integer] [--binomial] [--gaussian] [--p=float]
where the strings enclosed in square brackets are optional and can be used for different purposes. In particular:
- --N=integer sets the integer value of the number of balls N. If not provided, the default value is 500;
- --n=integer sets the dimension of the board n (or, equivantly, the number of cells in which the balls can fail). If not provided, the default value is 50;
- --binomial makes the program show the binomial approximation (with p = 0.5, see the report for more details), and its MSE with respect to the real data;
- --gaussian makes the program show the gaussian approximation of the binomial one;
- --p=float sets the probability, for each ball, of falling to the right at each of the n steps. If not provided, the default value is 0.5.

Notice that the version that has been used is python3.11. Different versions can require further installations of libraries (such as matplotlib, random, scipy) that are used in the script to achieve the provided results.

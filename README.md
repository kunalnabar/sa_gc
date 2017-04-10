# Simulated Annealing for Graph Coloring

# Description
This project implements Simulated Annealing as well as a variety of different graph generation methods to create graphs with known chromatic numbers in order to test the accuracy of the system. Much of this work was inpsired by *Optimization by Simulated Annealing: An Experimental Evaluation; Part II, Graph Coloring and Number Partitioning* by Johnson et al. A general description of simulated annealing can be found [here](https://en.wikipedia.org/wiki/Simulated_annealing).

This project was developed for MATH4630 at Vanderbilt University. All work represented here is my own. 

# Running the System
`python sa.py "gpath" "method"`
    gpath: the path to the graph of the adjacency matrix
        * The adjacency matrix should be in a text file, space delimited. It should be an unweighted, symmetric matrix.
    method: the method to be used to find neighboring solution sin the simulated annealing
        * 'penalty'/'p': using a penalty function
        * 'kempe'/'k': using finding the symmetric difference between two color classes and their Kempe chains to find two new disjoint sets
        * 'fixedk'/'k': a fixed number of color classes is selected and a solution is searched for using simulated annealing

The method will output information on it's execution to the console, including it's currently estimated chromatic number.
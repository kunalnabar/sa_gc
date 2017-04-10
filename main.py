# main.py
# kunal nabar

# library imports
import numpy as np
import sys
from copy import deepcopy

# personal imports
from structures import Graph

ptable = {}

chrom_est = []

def get_probability(key, T):
    if -(key)/T not in ptable:
        ptable[-(key)/T] = np.exp(-(key)/T)
    return ptable[-(key)/T]

def valid(G,S):
    for Ci in S:
        for i in Ci:
            for j in Ci:
                if G.has_edge(i,j):
                    return False
    return True

def simulated_annealing(G):
    T = INITIAL_T
    S = initial(G)
    print('inital state found.')
    S_lim = deepcopy(S)
    c_lim = np.inf
    c = cost(G,S)
    N = G.n
    freezecount = 0
    c_lim_change = False
    while freezecount < FREEZE_LIM:
        print('curr_cost %s' % (c_lim))
        changes = 0
        trials = 0
        while trials < SIZEFACTOR * N and changes < CUTOFF * N:
            trials = trials + 1
            Sp = neighbor(G,S)
            cp = cost(G,Sp)
            delta = cp - c
            if delta < 0: # downhill move
                changes = changes + 1
                c = cp
                S = Sp
                if cp < c_lim and valid(G,Sp):
                    S_lim = deepcopy(Sp)
                    c_lim_change = True
                    c_lim = cp
            else:
                ap = np.random.random()
                if ap <= get_probability(delta, T):
                    changes = changes + 1
                    S = Sp
                    c = cp
        T = TEMPFACTOR * T
        if c_lim_change:
            c_lim_change = False
            freezecount = 0
        if changes/trials < MINPERCENT:
            freezecount = freezecount + 1
        print('freezecount: %s, changes: %s, trials: %s' % (freezecount, changes, trials))
        print('current estimate: %s' % (len(S_lim)))
    return S_lim

if __name__ == '__main__':
    graph_file = sys.argv[1]
    approach = sys.argv[2]
    from parameters import params
    globals().update(params)
    if approach == 'penalty' or approach == 'p':
        from penalty import inital, neighbor, cost
    elif approach == 'kempe' or approach == 'k':
        from kempe import initial, neighbor, cost
    G = Graph(graph_file)
    S = simulated_annealing(G)
    X = len(S)
    print('est. chromatic number: %s' % (X))
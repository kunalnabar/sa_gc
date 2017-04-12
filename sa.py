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

def simulated_annealing(G,k=None):
    T = INITIAL_T
    S = initial(G,k)
    print('inital state found.')
    S_lim = deepcopy(S)
    c = cost(G,S)
    c_lim = c
    N = G.n
    freezecount = 0
    c_lim_change = False
    total_iterations = 0
    while freezecount < FREEZE_LIM:
        print('curr_cost %s' % (c_lim))
        changes = 0
        trials = 0
        while trials < SIZEFACTOR * N and changes < CUTOFF * N:
            trials = trials + 1
            Sp = neighbor(G,S)
            cp = cost(G,Sp)
            delta = cp - c
            if delta <= 0: # downhill move
                changes = changes + 1
                c = cp
                S = Sp
                #print('current cost= %s; lim= %s; isvalid=%s' % (cp, c_lim, valid(G,Sp)))
                if cp <= c_lim and valid(G,Sp) and len(Sp) <= len(S_lim):
                    #print('downhill move; isvalid=%s' % (valid(G,Sp)))
                    #print('current cost= %s; lim= %s' % (cp, c_lim))
                    S_lim = deepcopy(Sp)
                    if len(Sp) < len(S_lim): # check if it is strictly less
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
        if c_lim <= 0 and k != None:
            return S_lim
        if float(changes)/trials < MINPERCENT:
            freezecount = freezecount + 1
        total_iterations += 1
        print('%s freezecount: %s, changes/trials: %s' % (total_iterations, freezecount, float(changes)/trials))
        print('current estimate: %s' % (len(S_lim)))
    if k == None:
        return S_lim
    elif k != None and c_lim != 0:
        return [None]

if __name__ == '__main__':
    graph_file = sys.argv[1]
    approach = sys.argv[2]
    from parameters import params
    globals().update(params)
    k = None
    if approach == 'penalty' or approach == 'p':
        from penalty import initial, neighbor, cost
    elif approach == 'kempe' or approach == 'k':
        from kempe import initial, neighbor, cost
    elif approach == 'fixedk' or approach == 'f':
        from fixedk import initial, neighbor, cost
        k = int(sys.argv[3])
    G = Graph(graph_file)
    S = simulated_annealing(G,k)
    X = len(S)
    if S[0] == None:
        X = -1
    print('est. chromatic number: %s' % (X))
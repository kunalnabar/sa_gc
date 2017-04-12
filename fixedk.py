# fixedk.py
# kunalnabar

import numpy as np
from copy import deepcopy

def cost(G,S):
    E = np.zeros(len(S))
    for x in range(len(S)):
        for i in range(len(S[x])):
            for j in range(i+1, len(S[x])):
                if G.has_edge(S[x][i], S[x][j]):
                    E[x] += 1
    return E.sum()

def neighbor(G,S):
    # find random 'bad' vertex 
    # (i.e a vertex that is the endpoint of an 
    # edge that connects it to a vertex in it's color class)
    Sp = deepcopy(S)
    k = len(S)
    cc = -1
    v = -1
    for w in range(k):
        C = S[w]
        for i in range(len(C)):
            for j in range(i+1, len(C)):
                if G.has_edge(C[i], C[j]):
                    index = i
                    cc = w
            if v != -1:
                break
        if v != -1:
            break

    # move the element between color classes
    nc = cc
    while nc == cc: 
        nc = np.random.randint(k)
    if cc != -1:
        element = Sp[cc][index]
        del Sp[cc][index]
        Sp[nc].append(element)
    return Sp

def initial(G,k):
    S_initial = [[] for i in range(k)]
    vertices = range(G.n)
    i = 0
    j = 0
    for i in range(G.n):
        S_initial[j%k].append(i)
        j += 1
    return S_initial


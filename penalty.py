# penalty.py

import numpy as np
from copy import deepcopy

def cost(G,S):
    """The cost function for the penalty function approach
    The cost is defined as the sum of the square of the 
    color classes subtracted by the number of overlapping edges
    in each color class (i.e. two vertices in a color class share
    an edge) Note: this method does not enforce that each explored
    coloring be a valid coloring

    :param G: the graph
    :param S: the state to evaluate the cost of
    """
    # calculate negative sum of squares term
    Card = np.array([len(Ci) for Ci in S])
    SS = (Card**2).sum()
    # calculate sum of class size times edge overlap
    E = np.zeros(len(S))
    for x in range(len(S)):
        for i in range(len(S[x])):
            for j in range(i+1, len(S[x])):
                if G.has_edge(S[x][i], S[x][j]):
                    E[x] += 1
    return -SS + (E * Card * 2).sum()

def neighbor(G,S):
    """
    :param G: the graph
    :param S: the state to find a neighbor of
    """
    Sp = deepcopy(S)
    k = len(Sp)
    i = np.random.randint(0,k)
    j = i
    while j == i:
        j = np.random.randint(0,k+1)
    if j == k:
        Sp.append([])
    index = np.random.randint(0,len(Sp[i]))
    element = Sp[i][index]
    del Sp[i][index]
    Sp[j].append(element)
    if len(Sp[i]) == 0:
        del Sp[i]
    return Sp

def initial(G):
    """
    :param G: the graph
    """
    S_inital = []
    chunk_size = G.n / (G.max_degree + 1) + 1
    vertices = range(G.n)
    for i in range(0, G.n, chunk_size):
        S_inital.append(vertices[i:i+chunk_size])
    return S_inital

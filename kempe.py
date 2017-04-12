# kempe.py
# implementation of the kempe chain approach

import numpy as np
from copy import deepcopy

def cost(G,S):
    Card = np.array([len(Ci) for Ci in S])
    SS = (Card**2).sum()
    return -SS

def neighbor(G,S):
    restart = True
    c1,c2 = -1,-1
    while restart:
        # pick two empty color classes
        c1,c2 = np.random.choice(range(len(S)),size=2,replace=False)
        C,D = S[c1],S[c2]
        # do a bfs from v in color class C
        # find the kempe chain of C and D 
        # that contains v
        v = np.random.choice(C)
        KC = []
        Q = [v]
        while Q:
            length = len(Q)
            for i in range(length):
                vertex = Q[i]
                KC.append(vertex)
                adj_list = [u for u in 
                            np.where(G.adj_mat[vertex])[0] 
                            if (u in D
                            or u in C)
                            and (u not in KC
                            and u not in Q)]
                Q += adj_list
            Q = Q[length:]
        if set(KC) != set(C+D):
            restart = False
    # replace the color classes C and D
    # with the disjoint sets C symmetric difference KC
    # and D symmetric difference KC
    sym_dif1 = list(set(C).symmetric_difference(KC))
    sym_dif2 = list(set(D).symmetric_difference(KC))
    Sp = deepcopy(S)
    Sp[c1] = sym_dif1
    Sp[c2] = sym_dif2

    # delete any empty color classes
    # delete max index color class first
    # to maintain indices
    if not Sp[max(c1,c2)]:
        del Sp[max(c1,c2)]
    elif not Sp[min(c1,c2)]:
        del Sp[min(c1,c2)]
    return Sp
    

def initial(G,k=None):
    highest_color = 0
    vertex_colors = np.zeros(G.n) - 1
    for i in range(G.n):
        connections = np.where(G.adj_mat[i])[0]
        chosen_color = -1
        invalid_colors = []
        for index in connections:
            if vertex_colors[index] != -1:
                invalid_colors.append(vertex_colors[index])
        for potential_color in range(highest_color):
            if potential_color not in invalid_colors:
                chosen_color = potential_color
                break
        if chosen_color == -1:
            highest_color = highest_color + 1
            chosen_color = highest_color
        vertex_colors[i] = chosen_color
    S_initial = []
    for color in range(highest_color + 1):
        S_initial.append(list(np.where(vertex_colors == color)[0]))
    return S_initial

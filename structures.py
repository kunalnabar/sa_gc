import numpy as np
from itertools import combinations

class Graph(object):
    def __init__(self, adj_mat):
        if type(adj_mat) == str:
            self.adj_mat = np.loadtxt(adj_mat, dtype=int)
        else:
            self.adj_mat = adj_mat
        self.n = self.adj_mat.shape[0]
        self.m = int(self.adj_mat.sum()/2)
        self.max_degree = max(sum(self.adj_mat))
    def __repr__(self):
        return str(self.adj_mat)
    def has_edge(self, x, y):
        return self.adj_mat[x,y]
    def to_file(self,fname):
        import os
        np.savetxt(fname, self.adj_mat,fmt='%i')
        print('written to %s' % (os.path.abspath(fname)))

def mycielski(num_constructions):
    num_constructions = num_constructions - 2
    n = 3 * 2 ** num_constructions - 1
    start_length = 2
    adj_mat = np.zeros((n,n),dtype=int)
    adj_mat[0,1] = 1
    adj_mat[1,0] = 1
    it = 2
    for t in range(num_constructions):
        w = 2 * it
        for ui in range(it, it*2):
            vi = ui - it
            for ei in np.where(adj_mat[vi,0:it])[0]:
                adj_mat[ui, ei] = 1
                adj_mat[ei, ui] = 1
            adj_mat[w,ui] = 1
            adj_mat[ui,w] = 1
        it = 2 * it + 1
    return Graph(adj_mat)

def edge_probability(n,p):
    adj_mat = np.zeros((n,n))
    blk = np.zeros((n ** 2 - n)/2)
    blk[:int((n*(n - 1) / 2) * p)] = 1
    np.random.shuffle(blk)
    w = 0
    for i in range(n):
        for j in range(i+1, n):
            adj_mat[i,j] = blk[w]
            adj_mat[j,i] = blk[w]
            w = w + 1
    return Graph(adj_mat)

def kneser(n,k):
    comb = [set(element)
    for element in
    combinations(range(n), k)]
    n = len(comb)
    adj_mat = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if not comb[i].intersection(comb[j]):
                adj_mat[i,j] = 1
                adj_mat[j,i] = 1
    return Graph(adj_mat)
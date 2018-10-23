from Node import Node
from itertools import product

def Euclide_dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def Loo(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

class Graph:
    def loadFromFile(self, fname):
        with open(fname, 'r') as fin:
            N = self.N = int(fin.readline())
            S = tuple(map(int, fin.readline().split()))
            G = tuple(map(int, fin.readline().split()))

            self.nodes = {(i, j): Node((i, j)) for i, j in product(range(N), range(N))}
            
            map_mat = [fin.readline().split() for i in range(N)]

            for i, j in product(range(N), range(N)):
                self.nodes[(i, j)].isobstacle = map_mat[i][j] == '1'
                self.nodes[(i, j)].h = Euclide_dist((i, j), G)

            self.nodes[S].setStart()
            self.nodes[G].setGoal()
           
    def reset(self):
        for node in self.getNodes():
            node.reset()

    def lock(self):
        for node in self.getNodes():
            node.lock()

    def unlock(self):
        for node in self.getNodes():
            node.unlock()

    def getN(self):
        return self.N
    
    def getNodes(self):
        return self.nodes.values()
    
    def getNode(self, i, j = None):
        if j == None:
            return self.nodes[i]
        return self.nodes[(i, j)]
    
    def getStart(self):
        start = None
        for node in self.nodes.values():
            if node.isStart():
                if start:
                    raise "Multiple Starts"
                start = node
        if start is None:
            raise "Start not found"
        return start
    
    def getGoal(self):
        goal = None
        for node in self.getNodes():
            if node.isGoal():
                if goal:
                    raise "Multiple Goals"
                goal = node
        if goal is None:
            raise "Goal not found"
        return goal

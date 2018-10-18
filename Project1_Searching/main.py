import sys
from math import *
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from itertools import product
import time
import queue
import _thread
import threading

red = "background-color: red"
blue = "background-color: blue"
green = "background-color: green"
black = "background-color: black"
INF = 10 ** 9

CELL_SIZE = 60
 
class App(QDialog):
    def __init__(self):
        super().__init__()
        self.initGraph()
        self.left = 10
        self.top = 10
        self.width = self.graph.N * CELL_SIZE
        self.height = self.graph.N * CELL_SIZE + 20
        self.button = dict()
        self.initUI()
        self.solver = Solver(self.graph, self)
 
    def initGraph(self):
        self.graph = Graph()
        self.graph.loadFromFile('a.in')
        
    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createLayout()
        self.show()
 
    def createLayout(self):
        m = n = self.graph.N
        for i in range(n):
            for j in range(m):
                but = QPushButton("", self)
                but.setEnabled(False)
                but.setFixedSize(CELL_SIZE, CELL_SIZE)
                but.move(i * CELL_SIZE, j * CELL_SIZE)
                self.button[(j, i)] = but
        solve_but = QPushButton("solve", self)
        solve_but.move(0, n * CELL_SIZE)
        solve_but.clicked.connect(self.on_click)
    
    @pyqtSlot()
    def on_click(self):
        def foo():
            while self.solver.step():
                time.sleep(0.2)
            self.solver.trace()

        t = threading.Thread(target = foo)
        t.start()
#         t.join()
#         _thread.start_new_thread(foo, ())

def Euclide_dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def Loo(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

class Graph:
    def loadFromFile(self, fname):
        with open(fname, 'r') as fin:
            N = self.N = int(fin.readline())
            S = self.S = tuple(map(int, fin.readline().split()))
            G = self.G = tuple(map(int, fin.readline().split()))

            self.nodes = {(i, j): Node((i, j)) for i, j in product(range(N), range(N))}
            
            map_mat = [fin.readline().split() for i in range(N)]

            for i, j in product(range(N), range(N)):
                self.nodes[(i, j)].val = map_mat[i][j]
                self.nodes[(i, j)].h = Euclide_dist((i, j), G)
                
                if map_mat[i][j] != '1':
                    for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
                        x, y = i + dx, j + dy
                        if 0 <= x < N and 0 <= y < N and map_mat[x][y] != '1':
                            self.nodes[(i, j)].neighbors.append((self.nodes[(x, y)], 1))
            
            self.nodes[S].val = 'S'
            self.nodes[G].val = 'G'

class Node:
    def __init__(self, id):
        self.id = id
        self.neighbors = []
        self.dist = INF
        self.parent = None

    def __lt__(self, other):
        return self.id < other.id
        
    def setOpened(self):
        self.btn.setText(f'{self.dist:.2f}')
#         self.btn.setStyleSheet("background-color: blue")

    def setClosed(self):
        self.btn.setText(f'{self.dist:.2f}')
#         self.btn.setStyleSheet("background-color: red")

    def bindButton(self, but):
        self.btn = but
        if self.val == '1':
            but.setStyleSheet("background-color: black")
        elif self.val in 'SG':
            but.setStyleSheet("background-color: green")
            
    def setOnPath(self):
        pass
#         self.btn.setText('o')
        self.btn.setStyleSheet("background-color: green")
        
class Solver:
    def __init__(self, graph, app):
        self.bindGraph(graph, app)
        self.algo = self.a_star()

    def bindGraph(self, graph, app):
        self.graph = graph
        for node in graph.nodes.values():
            node.bindButton(app.button[node.id])

    def step(self):
        return self.algo.__next__()
    
    def trace(self):
        S = self.graph.nodes[self.graph.S]
        G = self.graph.nodes[self.graph.G]
        while G != None:
            print(G.id)
            G.setOnPath()
            G = G.parent

    # return False if stopped
    def dijkstra(self):
        S = self.graph.nodes[self.graph.S]
        G = self.graph.nodes[self.graph.G]
        S.dist = 0
        pq = queue.PriorityQueue()
        pq.put((0, S))
        while pq.qsize():
            cur_dist, cur = pq.get()

            if cur_dist != cur.dist:
                continue

            cur.setClosed()

            if cur == G:
                break
            
            for neighbor, weight in cur.neighbors:
                if neighbor.dist > cur.dist + weight:
                    neighbor.dist = cur.dist + weight
                    neighbor.setOpened()
                    pq.put((neighbor.dist, neighbor))
                    neighbor.parent = cur
                    yield True

        yield False
    
    def a_star(self):
        S = self.graph.nodes[self.graph.S]
        G = self.graph.nodes[self.graph.G]
        S.dist = S.h
        pq = queue.PriorityQueue()
        pq.put((S.h, S))
        while pq.qsize():
            cur_dist, cur = pq.get()

            if cur_dist != cur.dist:
                continue

            cur.setClosed()

            if cur == G:
                break

            for neighbor, weight in cur.neighbors:
                if neighbor.dist > cur.dist - cur.h + weight + neighbor.h:
                    neighbor.dist = cur.dist - cur.h + weight + neighbor.h
                    neighbor.setOpened()
                    pq.put((neighbor.dist, neighbor))
                    neighbor.parent = cur
                    yield True

        yield False
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

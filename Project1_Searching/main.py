import sys
from math import *
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QFileDialog
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
yellow = "background-color: rgb(255, 255, 0)"
INF = 10 ** 9

CELL_SIZE = 40
 
class App(QDialog):
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.buttons = dict()
        self.graph = None
        self.initUI()
 
    def initUI(self):
        self.setFixedSize(self.width, self.height)
        self.createLayout()
        self.show()

    def initBoard(self):
        if self.graph:
            m = n = self.graph.N
        else:
            m = self.width // CELL_SIZE
            n = self.height // CELL_SIZE
        
        for i in range(m):
            self.boardLayout.setColumnMinimumWidth(i, CELL_SIZE)

        for j in range(n):
            self.boardLayout.setRowMinimumHeight(j, CELL_SIZE)
            
        self.buttons = dict()
        for i in range(n):
            for j in range(m):
                but = QPushButton("", self)
                but.setEnabled(False)
                but.setFixedSize(CELL_SIZE, CELL_SIZE)
                self.buttons[(i, j)] = but
                self.boardLayout.addWidget(but, i, j)
                
    def createLayout(self):
        mainLayout = QVBoxLayout(self)

        self.boardLayout = QGridLayout()
        self.boardLayout.setSpacing(0)

        self.initBoard()

        controlLayout = QHBoxLayout()
        loadButton = QPushButton("Load graph", self)
        loadButton.clicked.connect(self.on_load)
        controlLayout.addWidget(loadButton)
        
        solve_but = QPushButton("Solve", self)
        solve_but.clicked.connect(self.on_solve)
        controlLayout.addWidget(solve_but)

        mainLayout.addLayout(self.boardLayout)
        mainLayout.addLayout(controlLayout)

        self.setLayout(mainLayout)

    @pyqtSlot()
    def on_solve(self):
        def foo():
            while self.solver.step():
                time.sleep(0.3)
            self.solver.trace()

        t = threading.Thread(target = foo)
        t.start()

    @pyqtSlot()
    def on_load(self):
        option = QFileDialog.Options()
        option |= QFileDialog.DontUseNativeDialog
        fname = QFileDialog.getOpenFileName(self, "Load graph", "", "Text files (*.txt, *.in)", options = option)[0]
        self.graph = Graph()
        self.graph.loadFromFile(fname)
        self.width = self.graph.N * CELL_SIZE
        self.height = self.graph.N * CELL_SIZE + CELL_SIZE
        QWidget().setLayout(self.layout())
        self.initUI()
        self.solver = Solver(self.graph, self)

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
        self.btn.setStyleSheet(blue)

    def setClosed(self):
        self.btn.setText(f'{self.dist:.2f}')
        self.btn.setStyleSheet(red)

    def bindButton(self, but):
        self.btn = but
        if self.val == '1':
            but.setStyleSheet(black)
        elif self.val in 'SG':
            but.setStyleSheet(green)
            
    def setOnPath(self):
        pass
#         self.btn.setText('o')
        self.btn.setStyleSheet(yellow)
        
class Solver:
    def __init__(self, graph, app):
        self.bindGraph(graph, app)
        self.algo = self.a_star()

    def bindGraph(self, graph, app):
        self.graph = graph
        for node in graph.nodes.values():
            node.bindButton(app.buttons[node.id])

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

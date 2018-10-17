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

red = "background-color: red"
blue = "background-color: blue"
green = "background-color: green"
black = "background-color: black"
INF = 10 ** 9

CELL_SIZE = 40
 
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
        _thread.start_new_thread(foo, ())

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
        
    def setOpened(self):
        self.btn.setText(str(self.dist))
        self.btn.setStyleSheet(blue)

    def setClosed(self):
        self.btn.setText(str(self.dist))
        self.btn.setStyleSheet(red)

    def bindButton(self, but):
        self.btn = but
        if self.val == '1':
            but.setStyleSheet(black)
        elif self.val in 'SG':
            but.setStyleSheet(green)

    def __lt__(self, other):
        return self.dist < other.dist
    
class Solver:
    def __init__(self, graph, app):
        self.bindGraph(graph, app)
        self.__stepper = self.__step()
        self.pq = queue.PriorityQueue()

    def bindGraph(self, graph, app):
        self.graph = graph
        for node in graph.nodes.values():
            node.bindButton(app.button[node.id])

    def step(self):
        return self.__stepper.__next__()

    # return True if stopped
    def __step(self):
        S = self.graph.nodes[self.graph.S]
        G = self.graph.nodes[self.graph.G]
        S.dist = 0
        self.pq.put((0, S))
        while self.pq.qsize():
            cur_dist, cur = self.pq.get()

            if cur_dist != cur.dist:
                continue

            cur.setClosed()
            
            if cur == G:
                break
            
            for neighbor, weight in cur.neighbors:
                print(neighbor.id, weight)
                if neighbor.dist > cur.dist + weight:
                    neighbor.dist = cur.dist + weight
                    neighbor.setOpened()
                    self.pq.put((neighbor.dist, neighbor))
                    yield True

        yield False
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

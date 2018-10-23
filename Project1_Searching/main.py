import sys
from math import *
from Solver import Solver
from Graph import Graph
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

CELL_SIZE = 40

class App(QDialog):
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 800
        self.buttons = dict()
        self.graph = None
        self.initUI()
 
    def initUI(self):
        self.setFixedSize(self.width, self.height)
        self.createLayout()
        self.show()

    def initBoard(self):
        if self.graph:
            m = n = self.graph.getN()
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
        
        start_but = QPushButton("Start", self)
        start_but.clicked.connect(self.on_start)
        controlLayout.addWidget(start_but)

#         stop_but = QPushButton("Stop", self)
#         stop_but.clicked.connect(self.on_stop)
#         controlLayout.addWidget(stop_but)

        reset_but = QPushButton("Reset", self)
        reset_but.clicked.connect(self.on_reset)
        controlLayout.addWidget(reset_but)
        self.reset_but = reset_but
        
        mainLayout.addLayout(self.boardLayout)
        mainLayout.addLayout(controlLayout)

        self.setLayout(mainLayout)
        
    def getChosenAlgo(self):
        return "A*"

    @pyqtSlot()
    def on_start(self):
        self.solver.start(self.getChosenAlgo())

    @pyqtSlot()
    def on_reset(self):
        self.solver.reset()

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

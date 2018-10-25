import sys
from math import *
from Solver import Solver
from Graph import Graph
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QFileDialog, QLabel, QDoubleSpinBox, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

CELL_SIZE = 20

class App(QDialog):
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 1000
        self.buttons = dict()
        self.graph = None
        self.initUI()
 
    def initUI(self):
        if self.layout():
            QWidget().setLayout(self.layout())
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
                font = but.font()
                font.setPointSize(int(CELL_SIZE * 0.2))
                but.setFont(font)
                self.buttons[(i, j)] = but
                self.boardLayout.addWidget(but, i, j)
                
    def createLayout(self):
        mainLayout = QVBoxLayout(self)

        self.boardLayout = QGridLayout()
        self.boardLayout.setSpacing(0)

        self.initBoard()

        graphControlLayout = QHBoxLayout()
        
        loadButton = QPushButton("Load graph", self)
        loadButton.clicked.connect(self.on_load)
        graphControlLayout.addWidget(loadButton)

        newButton = QPushButton("New graph")
        newButton.clicked.connect(self.on_new)
        graphControlLayout.addWidget(newButton)

        saveButton = QPushButton("Save graph")
        saveButton.clicked.connect(self.on_save)
        graphControlLayout.addWidget(saveButton)
        
        # -----------------------------------
        solverControlLayout = QHBoxLayout()

        epsLabel = QLabel("Set eps:", self)
        epsLabel.setMargin(0)
        solverControlLayout.addWidget(epsLabel)

        epsSpinBox = QDoubleSpinBox(self)
        epsSpinBox.setRange(1, 1000)
        epsSpinBox.setSingleStep(0.1)
        solverControlLayout.addWidget(epsSpinBox)

        timeLabel = QLabel("Set time:", self)
        solverControlLayout.addWidget(timeLabel)

        timeSpinBox = QDoubleSpinBox(self)
        timeSpinBox.setRange(0, 1000)
        timeSpinBox.setSingleStep(0.1)
        solverControlLayout.addWidget(timeSpinBox)

        heuristicLabel = QLabel("Heuristic:")
        solverControlLayout.addWidget(heuristicLabel)

        heuristicBox = QComboBox(self)
        heuristicBox.addItems(["C (Dijkstra)", "L2 (Euclidean)", "L1 (Manhattan)", "Loo"])
        solverControlLayout.addWidget(heuristicBox)
        
        start_but = QPushButton("Start", self)
        start_but.clicked.connect(self.on_start)
        solverControlLayout.addWidget(start_but, 2)
        
        reset_but = QPushButton("Reset", self)
        reset_but.clicked.connect(self.on_reset)
        solverControlLayout.addWidget(reset_but, 2)
        
        # -----------------------------------
        mainLayout.addLayout(self.boardLayout)
        mainLayout.addLayout(graphControlLayout)
        mainLayout.addLayout(solverControlLayout)

        self.setLayout(mainLayout)
        
    @pyqtSlot()
    def on_start(self):
        self.solver.start()

    @pyqtSlot()
    def on_reset(self):
        self.solver.reset()

    @pyqtSlot()
    def on_load(self):
        global CELL_SIZE
        option = QFileDialog.Options()
        option |= QFileDialog.DontUseNativeDialog
        fname = QFileDialog.getOpenFileName(self, "Load graph", "", "Text files (*.txt | *.in)", options = option)[0]
        self.graph = Graph()
        self.graph.loadFromFile(fname)
        CELL_SIZE = self.width // self.graph.getN()
        self.initUI()
        self.solver = Solver(self.graph, self)
    
    @pyqtSlot()
    def on_new(self):
        pass
    @pyqtSlot()
    def on_save(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

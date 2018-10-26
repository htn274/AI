import sys
from math import *
from Solver import Solver
from Graph import Graph
import Node
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class App(QDialog):
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.width = 950
        self.height = 1015
        self.cellSize = 50
        self.buttons = dict()
        self.graph = Graph(self.width // self.cellSize)
        self.initUI()
        self.solver = Solver(self)
        self.solver.bindGraph(self.graph, self)
        self.solver.colorChanged.connect(self.updateColor)
        self.solver.epsChanged.connect(self.updateEps)
        self.solver.timeChanged.connect(self.updateTime)
 
    def initUI(self):
        if self.layout():
            QWidget().setLayout(self.layout())
        self.setFixedSize(self.width, self.height)
        self.createLayout()
        self.show()

    def initBoard(self):
        if self.graph:
            n = self.graph.getN()
        
        for i in range(n):
            self.boardLayout.setColumnMinimumWidth(i, self.cellSize)
            self.boardLayout.setRowMinimumHeight(i, self.cellSize)
            
        self.buttons = dict()
        for i in range(n):
            for j in range(n):
                but = QPushButton("", self)
                but.setFixedSize(self.cellSize, self.cellSize)
                font = but.font()
                font.setPointSize(int(self.cellSize * 0.2))
                but.setFont(font)
                self.buttons[(i, j)] = but
                self.boardLayout.addWidget(but, i, j)

    @pyqtSlot(QPushButton, str)
    def updateColor(self, but, color):
        but.setStyleSheet(color)

    @pyqtSlot(float)
    def updateEps(self, newEps):
        self.curEpsValueLabel.setText(f'{newEps:.3f}')

    @pyqtSlot(float)
    def updateTime(self, elapsedTime):
        self.curTimeValueLabel.setText(f'{elapsedTime:.3f}')
                
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
        self.epsSpinBox = epsSpinBox
        solverControlLayout.addWidget(epsSpinBox)

        timeLabel = QLabel("Set time:", self)
        solverControlLayout.addWidget(timeLabel)

        timeSpinBox = QDoubleSpinBox(self)
        timeSpinBox.setRange(0.1, 1000)
        timeSpinBox.setSingleStep(0.1)
        self.timeSpinBox = timeSpinBox
        solverControlLayout.addWidget(timeSpinBox)

        heuristicLabel = QLabel("Heuristic:")
        solverControlLayout.addWidget(heuristicLabel)

        heuristicBox = QComboBox(self)
        heuristicBox.addItems(["Loo", "C (Dijkstra)", "L2 (Euclidean)", "L1 (Manhattan)"])
        self.heuristicBox = heuristicBox
        solverControlLayout.addWidget(heuristicBox)
        
        start_but = QPushButton("Solve", self)
        start_but.clicked.connect(self.on_start)
        solverControlLayout.addWidget(start_but, 2)

        stop_but = QPushButton("Stop", self)
        stop_but.clicked.connect(self.on_stop)
        solverControlLayout.addWidget(stop_but, 2)
        
        reset_but = QPushButton("Reset", self)
        reset_but.clicked.connect(self.on_reset)
        solverControlLayout.addWidget(reset_but, 2)
        
        # -----------------------------------
        infoLayout = QHBoxLayout(self)

        curEpsLabel = QLabel("Cur eps:", self)
        infoLayout.addWidget(curEpsLabel, 5)

        curEpsValueLabel = QLabel("1", self)
        infoLayout.addWidget(curEpsValueLabel, 5)
        self.curEpsValueLabel = curEpsValueLabel

        curTimeLabel = QLabel("Elapsed time:", self)
        infoLayout.addWidget(curTimeLabel, 5)

        curTimeValueLabel = QLabel("0", self)
        infoLayout.addWidget(curTimeValueLabel, 5)
        self.curTimeValueLabel = curTimeValueLabel

        startNodeInfoButton = QPushButton("Start", self)
        startNodeInfoButton.setStyleSheet(Node.START_COLOR)
        infoLayout.addWidget(startNodeInfoButton)

        goalNodeInfoButton = QPushButton("Goal", self)
        goalNodeInfoButton.setStyleSheet(Node.GOAL_COLOR)
        infoLayout.addWidget(goalNodeInfoButton)

        emptyNodeInfoButton = QPushButton("Empty", self)
        emptyNodeInfoButton.setStyleSheet(Node.EMPTY_COLOR)
        infoLayout.addWidget(emptyNodeInfoButton)

        obstacleNodeInfoButton = QPushButton("Obstacle", self)
        obstacleNodeInfoButton.setStyleSheet("color: white;" + Node.OBSTACLE_COLOR)
        infoLayout.addWidget(obstacleNodeInfoButton)

        openedNodeInfoButton = QPushButton("Opened", self)
        openedNodeInfoButton.setStyleSheet(Node.OPEN_COLOR)
        infoLayout.addWidget(openedNodeInfoButton)
        
        closedNodeInfoButton = QPushButton("Closed", self)
        closedNodeInfoButton.setStyleSheet(Node.CLOSED_COLOR)
        infoLayout.addWidget(closedNodeInfoButton)
        
        onPathNodeInfoButton = QPushButton("On path", self)
        onPathNodeInfoButton.setStyleSheet(Node.ON_PATH_COLOR)
        infoLayout.addWidget(onPathNodeInfoButton)
        
        # ------------------------------------
        mainLayout.addLayout(self.boardLayout)
        mainLayout.addLayout(graphControlLayout)
        mainLayout.addLayout(solverControlLayout)
        mainLayout.addLayout(infoLayout)

        self.setLayout(mainLayout)
        
    @pyqtSlot()
    def on_start(self):
        self.solver.reset()
        self.solver.solve(eps = float(self.epsSpinBox.value()),\
                          time = float(self.timeSpinBox.value()),\
                          heuristic = self.heuristicBox.currentText().split()[0])

    @pyqtSlot()
    def on_reset(self):
        self.solver.reset()

    @pyqtSlot()
    def on_load(self):
        option = QFileDialog.Options()
        option |= QFileDialog.DontUseNativeDialog
        fname = QFileDialog.getOpenFileName(self, "Load graph", "", "Text files (*.txt | *.in)", options = option)[0]
        self.graph = Graph()
        self.graph.loadFromFile(fname)
        self.cellSize = self.width // self.graph.getN()
        self.initUI()
        self.solver.bindGraph(self.graph, self)
    
    @pyqtSlot()
    def on_new(self):
        N, ok = QInputDialog.getInt(self, "New graph", "N =")
        if ok:
            self.graph = Graph(N)
            self.cellSize = self.width // N
            self.initUI()
            self.solver.bindGraph(self.graph, self)
            
    @pyqtSlot()
    def on_save(self):
        fname, ok = QInputDialog.getText(self, "Save graph", "Graph name:")
        if ok:
            self.graph.save(fname)
            
    @pyqtSlot()
    def on_stop(self):
        self.solver.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

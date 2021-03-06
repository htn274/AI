import time as thread_time
INF = 10 ** 9

RED = "background-color: red"
BLUE = "background-color: blue"
GREEN = "background-color: green"
BLACK = "background-color: black"
WHITE = "background-color: white"
YELLOW = "background-color: rgb(255, 255, 0)"
CYAN = "background-color: cyan"

START_COLOR = GREEN
GOAL_COLOR = CYAN
OBSTACLE_COLOR = BLACK
EMPTY_COLOR = WHITE
ONPATH_COLOR = YELLOW
CLOSED_COLOR = RED
OPENED_COLOR = BLUE

class Node:
    def __init__(self, id):
        self.id = id # tuple of (x, y)
        
        self.h = 0
        self.g = INF
        
        self.parent = None
        
        self.locked = False
        self.isobstacle = False
        
        self.isstart = False
        self.isgoal = False
        
        self.btn = None

        self.colorUpdater = None
        
    def getF(self, eps = 1):
        return self.getG() + eps * self.getH()
    
    # g get/set
    def setG(self, g):
        self.g = g
    def getG(self):
        return self.g

    # h get/set
    def setH(self, h):
        self.h = h
    def getH(self):
        return self.h
    
    # Parent set/get
    def setParent(self, par):
        self.parent = par
    def getParent(self):
        return self.parent
    
    # isStart get/set
    def setStart(self):
        self.isobstacle = False
        self.isstart = True
        self.isgoal = False
        self.setColor(START_COLOR)
    def isStart(self):
        return self.isstart

    # isGoal get/set
    def setGoal(self):
        self.isobstacle = False
        self.isgoal = True
        self.isstart = False
        self.setColor(GOAL_COLOR)
    def isGoal(self):
        return self.isgoal

    # get X, Y (no set's)
    def getX(self):
        return self.id[0]
    def getY(self):
        return self.id[1]
    
    def __lt__(self, other):
        return self.id < other.id

    def reset(self):
        self.parent = None
        self.locked = False
        self.g = INF
#         self.h = 0
        self.btn.setText('')
        self.bindButton(self.btn)

    # confirm that this is opened
    def setOpened(self):
        self.setColor(OPENED_COLOR)

    def setClosed(self):
        self.setColor(CLOSED_COLOR)

    # lock get/set: true if algorithm is running
    def lock(self):
        self.locked = True
    def unlock(self):
        self.locked = False
    def isLocked(self):
        return self.locked

    # called when it's button is pressed
    def changeState(self):
        if not self.isLocked():
            if self.isObstacle():
                self.setStart()
            elif self.isStart():
                self.setGoal()
            elif self.isGoal():
                self.setEmpty()
            else:
                self.setObstacle()
    
    def bindButton(self, but):
        self.btn = but
        if self.isObstacle():
            self.setObstacle()
        elif self.isStart():
            self.setStart()
        elif self.isGoal():
            self.setGoal()
        else:
            self.setEmpty()
            
    # is obstacle get/set
    def setObstacle(self):
        if not self.isLocked():
            self.isobstacle = True
            self.isstart = self.isgoal = False
            self.setColor(OBSTACLE_COLOR)
            
    def isObstacle(self):
        return self.isobstacle
        
    # set normal cell
    def setEmpty(self):
        if not self.isLocked():
            self.isobstacle = self.isstart = self.isgoal = False
            self.setColor(EMPTY_COLOR)
        
    def setColor(self, color):
        if self.colorUpdater:
            self.colorUpdater.updateColor(self, color)
    def getColor(self):
        return self.color
        
    def setOnPath(self):
        self.setColor(ONPATH_COLOR)

    def setText(self, text):
        self.btn.setText(text)

    def invalidate(self):
        return
        self.btn.repaint()

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
ON_PATH_COLOR = YELLOW
CLOSED_COLOR = red


class Node:
    def __init__(self, id):
        self.id = id
        self.dist = INF
        self.parent = None
        self.locked = False
        self.isobstacle = False
        self.start = False
        self.goal = False
        self.btn = None

    def setStart(self):
        self.isobstacle = False
        self.start = True
        self.goal = False
        self.setColor(START_COLOR)
    
    def isStart(self):
        return self.start

    def setGoal(self):
        self.isobstacle = False
        self.goal = True
        self.start = False
        self.setColor(GOAL_COLOR)

    def isGoal(self):
        return self.goal

    def getX(self):
        return self.id[0]

    def getY(self):
        return self.id[1]
    
    def __lt__(self, other):
        return self.id < other.id

    def reset(self):
        self.dist = INF
        self.parent = None
        self.locked = False
        self.btn.setText('')
        self.bindButton(self.btn)

    def setOpened(self):
        self.btn.setText(f'{self.dist:.2f}')
        self.btn.setStyleSheet(blue)

    def setClosed(self):
        self.btn.setText(f'{self.dist:.2f}')
        self.setColor(CLOSED_COLOR)

    def lock(self):
        self.locked = True

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

    def isLocked(self):
        return self.locked

    def unlock(self):
        self.locked = False

    def bindButton(self, but):
        self.btn = but
        if self.isObstacle():
            self.setColor(OBSTACLE_COLOR)
        else:
            self.setColor(EMPTY_COLOR)
            
    def setObstacle(self):
        if not self.isLocked():
            self.isobstacle = True
            self.start = self.goal = False
            self.setColor(OBSTACLE_COLOR)

    def isObstacle(self):
        return self.isobstacle
        
    def setEmpty(self):
        if not self.isLocked():
            self.isobstacle = self.start = self.goal = False
            self.setColor(EMPTY_COLOR)
        
    def setColor(self, color):
        if self.btn:
            self.btn.setStyleSheet(color)
        
    def setOnPath(self):
        self.setColor(ON_PATH_COLOR)

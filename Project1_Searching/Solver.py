from Graph import Graph
import threading
import time as thread_time
from itertools import product
import queue
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

INF = 10 ** 9
SLEEP_TIME = 0.005

def onNodeClicked(node):
    @pyqtSlot()
    def foo():
        node.changeState()
    return foo
    
class Solver(QThread):
    colorChanged = pyqtSignal(QPushButton, str)
    epsChanged = pyqtSignal(float)
    timeChanged = pyqtSignal(float)
    
    def __init__(self, app):
        super(Solver, self).__init__(app)
        self.running = False

    def updateColor(self, node, color):
        self.colorChanged.emit(node.btn, color)

    def updateEps(self, eps):
        self.epsChanged.emit(eps)

    def updateTime(self, elapsedTime):
        self.timeChanged.emit(elapsedTime)
        
    def bindGraph(self, graph, app):
        self.graph = graph
        for node in graph.nodes.values():
            but = app.buttons[node.id]
            node.colorUpdater = self
            node.bindButton(but)
            but.clicked.connect(onNodeClicked(node))

    def C(self, a, b):
        return 0
    def L2(self, a, b):
        return ((a.getX() - b.getX()) ** 2 + (a.getY() - b.getY()) ** 2) ** 0.5
    def L1(self, a, b):
        return abs(a.getX() - b.getX()) + abs(a.getY() - b.getY())
    def Loo(self, a, b):
        return max(abs(a.getX() - b.getX()), abs(a.getY() - b.getY()))

    def run(self):
        lastTime = thread_time.time()
        totalTime = 0
        while self.step() and self.running:
            totalTime += thread_time.time() - lastTime
            self.updateTime(totalTime)
            if totalTime > self.time:
                break
            thread_time.sleep(SLEEP_TIME)
            lastTime = thread_time.time()
        self.publishSolution()
        self.graph.unlock()
        self.running = False
        self.quit()
            
    def solve(self, eps, time, heuristic):
        if not self.running:
            self.eps = eps
            self.time = time
            self.heuristic = eval("self." + heuristic)
            self.running = True
            self.algo = self.ara_star()
            self.graph.lock()
            self.start()
                    
    def stop(self):
        self.running = False
        
    def reset(self):
        self.running = False
        thread_time.sleep(0.1)
        self.graph.reset()
        self.graph.getStart().setStart()
        self.graph.getGoal().setGoal()

    def step(self):
        return self.algo.__next__()
    
    def publishSolution(self):
        S = self.graph.getStart()
        G = self.graph.getGoal()
        while G != None:
            G.setOnPath()
            G = G.parent

    
    
    def ara_star(self):
        def updateHeuristic():
            for node in self.graph.getNodes():
                node.setH(self.heuristic(node, G))
                
        def improvePath():
            N = self.graph.getN()
            
            while OPEN.qsize():
                f_value, s = OPEN.get()

                if G.getF(eps) <= f_value:
                    break

                # CLOSED = CLOSED U s
                CLOSED.add(s)
                s.setClosed()
                s.setText(f'{s.getF(eps):.2f}')
                yield

                for (dx, dy) in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
                    x, y = s.getX() + dx, s.getY() + dy
                    if (x, y) not in product(range(N), range(N)):
                        continue
                    neighbor = self.graph.getNode(x, y)
                    if neighbor.isObstacle():
                        continue

                    if s.getG() + 1 < neighbor.getG():
                        neighbor.setG(s.getG() + 1)
                        neighbor.setOpened()
                        neighbor.setText(f'{neighbor.getF(eps):.2f}')
                        yield
                        neighbor.setParent(s)
                        if neighbor not in CLOSED:
                            OPEN.put((neighbor.getF(eps), neighbor))
                        else:
                            INCONS.append(neighbor)
        
        def moveInconsToOpen():
            while len(INCONS):
                OPEN.put((0, INCONS.pop()))

        def updateOpen():
            nonlocal OPEN
            OPEN_update = queue.PriorityQueue()
            for _, s in OPEN.queue:
                OPEN_update.put((s.getF(eps), s))
                s.setText(f'{s.getF(eps):.2f}')

            OPEN = OPEN_update

        def min_g_h():
            OPEN_U_INCONS = {s for _, s in OPEN.queue} | INCONS
            return min(s.getF() for s in OPEN_U_INCONS) 
        
        def removePathColor():
            S = self.graph.getStart()
            G = self.graph.getGoal()
            while G != None:
                G.setClosed()
                G = G.parent
        
        OPEN = queue.PriorityQueue()
        S = self.graph.getStart()
        G = self.graph.getGoal()

        updateHeuristic()

        S.setG(0)
        
        CLOSED = set()
        INCONS = []
        
        eps = self.eps
        self.updateEps(eps)
        OPEN.put((S.getF(eps), S))
        S.setOpened()
        S.setText(f'{S.getF(eps):.2f}')
        yield True

        for _ in improvePath():
            yield True

        eps = min(eps, G.getG() / min_g_h())
        self.updateEps(eps)

        self.publishSolution()
        yield True
        
        while eps > 1:
            removePathColor()
            eps *= 0.9
            self.updateEps(eps)
            
            moveInconsToOpen()

            updateOpen()

            CLOSED = set()
            for _ in improvePath():
                yield True
            
            eps = min(eps, G.getG() / min_g_h())
            self.updateEps(eps)

            self.publishSolution()
            
            yield True

        yield False




# def a_star(self):
#         def updateHeuristic():
#             for node in self.graph.getNodes():
#                 node.setH(self.heuristic(node, G))
#                 print(node.id, node.getH())
#         S = self.graph.getStart()
#         G = self.graph.getGoal()
#         updateHeuristic()
#         S.setG(0)
#         S.setText(f'{S.getF():.2f}')
#         OPEN = queue.PriorityQueue()
#         OPEN.put((S.h, S))
#         while OPEN.qsize():
#             cur_F, cur = OPEN.get()
# 
#             if cur_F != cur.getF():
#                 continue
# 
#             cur.setClosed()
# 
#             print(cur.id)
#             if cur == G:
#                 break
# 
#             for (dx, dy) in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
#                 x, y = cur.getX() + dx, cur.getY() + dy
#                 if (x, y) not in product(range(self.graph.N), range(self.graph.N)):
#                     continue
#                 neighbor = self.graph.getNode(x, y)
#                 if neighbor.isObstacle():
#                     continue
#                 print(neighbor.id)
#                 if neighbor.getF() > cur.getF() - cur.h + 1 + neighbor.h:
# #                     neighbor.setF(cur.getF() - cur.h + 1 + neighbor.h)
#                     neighbor.setG(cur.getG() + 1)
#                     neighbor.setOpened()
#                     neighbor.setText(f'{neighbor.getF():.2f}')
#                     OPEN.put((neighbor.getF(), neighbor))
#                     neighbor.setParent(cur)
# #                     yield True
# 
#         self.publishSolution()
#         yield False

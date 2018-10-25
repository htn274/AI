from Graph import Graph
import threading
import time
from itertools import product
import queue
from PyQt5.QtCore import pyqtSlot

INF = 10 ** 9
SLEEP_TIME = 0.

def onNodeClicked(node):
    @pyqtSlot()
    def foo():
        node.changeState()
    return foo
    
class Solver:
    def __init__(self, graph, app):
        self.bindGraph(graph, app)
        self.started = False

    def bindGraph(self, graph, app):
        self.graph = graph
        for node in graph.nodes.values():
            but = app.buttons[node.id]
            node.bindButton(but)
            but.clicked.connect(onNodeClicked(node))
        self.graph.getStart().setStart()
        self.graph.getGoal().setGoal()
            

    def start(self):
        if not self.started:
            self.started = True
            self.algo = self.a_star()
            def foo():
                while self.step():
                    time.sleep(SLEEP_TIME)
                self.graph.unlock()
            t = threading.Thread(target = foo)
            t.start()
                    
    def reset(self):
        self.graph.reset()

    def step(self):
        return self.algo.__next__()
    
    def publishSolution(self):
        S = self.graph.getStart()
        G = self.graph.getGoal()
        while G != None:
            print(G.id)
            G.setOnPath()
            G = G.parent

    def a_star(self):
        self.graph.lock()
        S = self.graph.getStart()
        G = self.graph.getGoal()
        S.setG(0)
        S.setText(f'{S.getF():.2f}')
        OPEN = queue.PriorityQueue()
        OPEN.put((S.h, S))
        while OPEN.qsize():
            cur_F, cur = OPEN.get()

            if cur_F != cur.getF():
                continue

            cur.setClosed()

            if cur == G:
                print("sad")
                break

            for (dx, dy) in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
                x, y = cur.getX() + dx, cur.getY() + dy
                if (x, y) not in product(range(self.graph.N), range(self.graph.N)):
                    continue
                neighbor = self.graph.getNode(x, y)
                if neighbor.isObstacle():
                    continue
                if neighbor.getF() > cur.getF() - cur.h + 1 + neighbor.h:
#                     neighbor.setF(cur.getF() - cur.h + 1 + neighbor.h)
                    neighbor.setG(cur.getG() + 1)
                    neighbor.setOpened()
                    neighbor.setText(f'{neighbor.getF():.2f}')
                    OPEN.put((neighbor.getF(), neighbor))
                    neighbor.setParent(cur)
                    yield True

        self.publishSolution()
        yield False
    
    def ara_star(self):
        
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
                        neighbor.setParent(s)
                        if neighbor not in CLOSED:
                            OPEN.put((neighbor.getF(eps), neighbor))
                        else:
                            INCONS.append(neighbor)
        
        def moveInconsToOpen():
            while len(INCONS):
                OPEN.put((0, INCONS.pop()))

        OPEN = queue.PriorityQueue()
        def updateOpen(OPEN):
            OPEN_update = queue.PriorityQueue()
            for _, s in OPEN.queue:
                OPEN_update.put((s.getF(eps), s))
                s.setText(f'{s.getF(eps):.2f}')

            return OPEN_update

        def min_g_h():
            if OPEN.qsize():
                min_g_h_OPEN = min(s.getF() for _, s in OPEN.queue)
            else:
                min_g_h_OPEN = INF

            if len(INCONS):
                min_g_h_INCONS = min(s.getF() for s in INCONS)
            else:
                min_g_h_INCONS = INF

            return min(min_g_h_OPEN, min_g_h_INCONS)
        
        def removePathColor():
            S = self.graph.getStart()
            G = self.graph.getGoal()
            while G != None:
                G.setClosed()
                G = G.parent
        
        self.graph.lock()
        S = self.graph.getStart()
        G = self.graph.getGoal()

        S.setG(0)
        
        CLOSED = set()
        INCONS = []
        
        eps = 2
        OPEN.put((S.getF(eps), S))
        S.setOpened()
        S.setText(f'{S.getF(eps):.2f}')

        improvePath()

        eps = min(eps, G.getG() / min_g_h())

        self.publishSolution()
        
        yield True

        while eps > 1:
            removePathColor()
            eps *= 0.9

            moveInconsToOpen()

            OPEN = updateOpen(OPEN)

            CLOSED = set()
            improvePath()
            
            eps = min(eps, G.getG() / min_g_h())

            self.publishSolution()
            yield True

        yield False

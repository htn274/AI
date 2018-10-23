from Graph import Graph
import threading
import time
from itertools import product
import queue
from PyQt5.QtCore import pyqtSlot

SLEEP_TIME = 0.3

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
            

    def start(self, algo):
        if not self.started:
            self.started = True
            self.algo = {"A*": self.a_star, "Dijkstra": self.dijkstra}[algo]()
            def foo():
                while self.step():
                    time.sleep(SLEEP_TIME)
                self.trace()
                self.graph.unlock()
            t = threading.Thread(target = foo)
            t.start()
                    
    def reset(self):
        self.graph.reset()

    def step(self):
        return self.algo.__next__()
    
    def trace(self):
        S = self.graph.getStart()
        G = self.graph.getGoal()
        while G != None:
            print(G.id)
            G.setOnPath()
            G = G.parent

    # return False if stopped
    def dijkstra(self):
        self.graph.lock()
        S = self.graph.getStart()
        G = self.graph.getGoal()
        
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
            
            for (dx, dy) in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
                nid = (cur.id[0] + dx, cur.id[1] + dy)
                if nid not in product(range(self.graph.N), range(self.graph.n)):
                    continue
                neighbor = self.graph.nodes[nid]
                if neighbor.isObstacle:
                    continue
                if neighbor.dist > cur.dist + 1:
                    neighbor.dist = cur.dist + 1
                    neighbor.setOpened()
                    pq.put((neighbor.dist, neighbor))
                    neighbor.parent = cur
                    yield True

        yield False
    
    def a_star(self):
        self.graph.lock()
        S = self.graph.getStart()
        G = self.graph.getGoal()
        S.dist = S.h
        OPEN = queue.PriorityQueue()
        OPEN.put((S.h, S))
        while OPEN.qsize():
            cur_dist, cur = OPEN.get()

            if cur_dist != cur.dist:
                continue

            cur.setClosed()

            if cur == G:
                break

            for (dx, dy) in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
                nid = (cur.id[0] + dx, cur.id[1] + dy)
                if nid not in product(range(self.graph.N), range(self.graph.N)):
                    continue
                neighbor = self.graph.nodes[nid]
                if neighbor.isObstacle:
                    continue
                if neighbor.dist > cur.dist - cur.h + 1 + neighbor.h:
                    neighbor.dist = cur.dist - cur.h + 1 + neighbor.h
                    neighbor.setOpened()
                    OPEN.put((neighbor.dist, neighbor))
                    neighbor.parent = cur
                    yield True

        yield False


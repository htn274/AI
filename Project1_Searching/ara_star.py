import time
import itertools
import queue as Q

"""returns the Euclidian distance of (ax, ay) and (bx, by)"""
def Euclide_dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

"""Infomation of the search request
@S: start pos
@G: goal pos
@time_limit: time to run a*
@epsilon: epsilon
@start_time: time when start run a*
@total_time: time result
"""
class Request:
    def __init__(self, start, goal, timelimit, eps):
        self.S = start
        self.G = goal
        self.time_limit = timelimit
        self.epsilon = eps
        self.start_time = 0
        self.total_time = 0
        self.Solutions = []

    def go(self):
        self.start_time = time.clock()

    def finished(self):
        self.total_time += time.clock() - self.start_time

    def total_search_time(self):
        return self.total_time

class Progress_info:
    def __init__(self):
        self.goal_found = False
        self.best_path = []
        self.INCONS = set([])
        self.OPEN = Q.PriorityQueue()
        self.costs = {} #g(x)
    
def improve_path(mat, request, progress):
    # node opening order
    DIRs = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]

    N = len(mat)
    CLOSED = {}

    pre = {S: S}
    epsilon = request.epsilon

    while (True):
        _, f_value = progress.OPEN[0]
        if (not progress.goal_found and \
        progress.costs[request.G] + epsilon * h[request.G] > f_value):
            break
        
        if (progress.OPEN.qsize()):
            result.path = []
            request.Solutions.append(result)
            print("No solution found by improve_path.")
            return False

        #remove s with smallest fvalue from OPEN
        s, f_value = progress.OPEN.get()
        x, y = s
        #CLOSED = CLOSED U s
        CLOSED.add(s)
        
        #traverse child of s
        for dx, dy in DIRs:
            neighbor_node = (x + dx, y + dy)

            if 0 <= x + dx < N and 0 <= y + dy < N\
                and mat[x + dx][y + dy] != 1\
                and progress.costs[s] + 1 < progress.costs.get(neighbor_node, INF):
                    progress.costs[neighbor_node] = progress.costs[s] + 1
                    pre[neighbor_node] = s
                    if (neighbor_node not in CLOSED):
                        progress.OPEN.put({progress.costs[neighbor_node] + epsilon * h[neighbor_node], neighbor_node})
                    else:
                        progress.INCONS.add(neighbor_node)

    if G not in pre:
        return False
    path = [G]
    while G != S:
        G = pre[G]
        path.append(G)

    if (path != progress.best_path):
        progress.best_path = path

    return True

def min_g_h(progress, request):
    return 0

"""
@mat: input matrix 
@request: search request
"""
def ara_star(mat, request):
    request.go()
    
    progress = Progress_info()
    #g(Goal) = inf; g(Start) = 0
    progress.costs[request.S] = 0
    progress.costs[request.G] = INF
    progress.OPEN.put({h[request.S] * request.epsilon, request.S})

    progress.goal_found = improve_path(mat, request, progress)
    if (progress.OPEN.qsize()):
        request.finished()
        print("No solution found after ", request.total_search_time(), "ms")
        return
    
    #publish solution
    print("Epsilon: ", request.epsilon)
    print("Path: ")
    print(progress.best_path)

    request.epsilon = min(request.epsilon, progress.costs[request.G]/min_g_h(progress))

    while (request.epsilon > 1):
        request.epsilon -= 0.5
        #Move states from INCONS into OPEN
        for incons in progress.INCONS:
            progress.OPEN.put({0, incons})
        progress.INCONS = []
        #Update priorities for all s in OPEN
        OPEN_update = Q.PriorityQueue()
        for s, f_value in progress.OPEN:
            OPEN_update.put(progress.costs[s] + h[s] * request.epsilon)
        
        progress.OPEN = OPEN_update

        progress.goal_found = improve_path(mat, request, progress)
        request.epsilon = min(request.epsilon, progress.costs[request.G]/min_g_h(progress))

        #publish solution
        print("Epsilon: ", request.epsilon)
        print("Path: ")
        print(progress.best_path)
    

# heuristic function
    h = {(x, y): Euclide_dist((x, y), request.S) for x, y in itertools.product(range(N), range(N))}
    
request = Request((0, 1), (3, 3), 1, 1.0)





    
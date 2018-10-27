import time
import itertools
import queue as Q
import argparse

INF = 10 ** 9
"""returns the Euclidian distance of (ax, ay) and (bx, by)"""
def Euclide_dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

"""returns the Diagnol distance of (ax, ay) and (bx, by)"""
def Loo(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

"""Infomation of the search request
@mat: matrix input
@S: start pos
@G: goal pos
@time_limit: time to run a*
@epsilon: epsilon
@start_time: time when start run a*
@total_time: time result
"""
class Request:
    def __init__(self, ma, start, goal, timelimit, eps):
        self.mat = ma
        self.S = start
        self.G = goal
        self.time_limit = timelimit
        self.epsilon = eps
        self.start_time = 0
        self.total_time = 0
        self.Solutions = []
    #Start timer
    def go(self):
        self.start_time = time.clock()
    #Calculate total time
    def finished(self):
        self.total_time += time.clock() - self.start_time

"""
Information of the progress 
@goal_found: check whether the Goal can be reached
@best_path: the most optimal path
@INCONS
@OPEN
@costs: g(x)
@pre: 
"""
class Progress_info:
    def __init__(self):
        self.goal_found = False
        self.best_path = []
        self.INCONS = set()
        self.OPEN = Q.PriorityQueue()
        self.costs = {}
        self.pre = {}
    
"""
Information of the solution
@time: total time 
@eps: the last epsilon
@path: the most optimal path with the last epsilon
"""
class Solution:
    def __init__(self, time, eps, path):
        self.time = time
        self.epsilon = eps
        self.path = path

    def output(self, fout, request):
        fout.write("Time: " + str(self.time) + "\n")
        fout.write("Epsilon: " + str(self.epsilon) + "\n")
        fout.write(str(len(self.path)) + "\n")
        fout.write(' '.join(list(f'({x},{y})' for (x, y) in self.path)) + '\n')
        N = len(request.mat)
        for x in range(N):
                for y in range(N):
                    if (x, y) == request.S:
                        fout.write('S')
                    elif (x, y) == request.G:
                        fout.write('G')
                    elif (x, y) in self.path:
                        fout.write('x')
                    else:
                        fout.write('-' if request.mat[x][y] == 0 else 'o')
                fout.write('\n')
        
"""
@mat: input matrix 
@request: 
@progress: infomation of current progress
"""
def improve_path(request, progress):
    # node opening order
    DIRs = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]

    mat = request.mat
    N = len(mat)
    CLOSED = set([])

    epsilon = request.epsilon

    while progress.OPEN.qsize():
        f_value, _ = progress.OPEN.queue[0]
        if progress.costs[request.G]  + epsilon * h[request.G] <= f_value:
            break

        #remove s with smallest fvalue from OPEN
        f_value, s = progress.OPEN.get()
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
                    progress.pre[neighbor_node] = s
                    if (neighbor_node not in CLOSED):
                        progress.OPEN.put((progress.costs[neighbor_node] + epsilon * h[neighbor_node], neighbor_node))
                    else:
                        progress.INCONS.add(neighbor_node)
    
    if request.G not in progress.pre:
        return False
    path = [request.G]
    node = request.G
    while node != request.S:
        node = progress.pre[node]
        path.append(node)

    if (path != progress.best_path):
        progress.best_path = path
    
    return True

"""
Find min INCONS U OPEN (g + h)
"""
def min_g_h(progress):
    OPEN_U_INCONS = {s for _, s in progress.OPEN.queue} | progress.INCONS
    return min(progress.costs[s] + h[s] for s in OPEN_U_INCONS) 


"""
@mat: input matrix 
@request: search request
"""
def ara_star(request, fout):
    request.go()
    
    progress = Progress_info()
    #g(Goal) = inf; g(Start) = 0
    progress.costs = {request.S : 0}
    progress.costs[request.G] = INF
    progress.pre = {request.S: request.S}
    progress.OPEN.put((h[request.S] * request.epsilon, request.S))

    progress.goal_found = improve_path(request, progress)

    if not progress.goal_found:
        request.finished()
        fout.write("-1")
        fout.write("Time: " + str(request.total_time))
        #print("No solution found after ", request.total_search_time(), "ms")
        return

    eps = min(request.epsilon, progress.costs[request.G]/min_g_h(progress))

    #publish solution
    request.finished()
    """
    sol = Solution(request.total_time, eps, progress.best_path[::-1])
    sol.output(fout)
    """

    while (request.total_time < request.time_limit and eps > 1):
        request.epsilon -= 0.25
        #Move states from INCONS into OPEN
        for incons in progress.INCONS:
            progress.OPEN.put((0, incons))
        progress.INCONS = set([])
        #Update priorities for all s in OPEN
        OPEN_update = Q.PriorityQueue()
        for f_value, s in progress.OPEN.queue:
            OPEN_update.put((progress.costs[s] + h[s] * request.epsilon, s))
        progress.OPEN = OPEN_update
        #Improve path
        progress.goal_found = improve_path(request, progress)
        #get new epsilon
        eps = min(request.epsilon, progress.costs[request.G]/min_g_h(progress))

        #publish solution
        request.finished()
        """
        sol = Solution(request.total_time, eps, progress.best_path[::-1])
        sol.output(fout)
        """
    sol = Solution(request.total_time, eps, progress.best_path[::-1])
    sol.output(fout, request)

if __name__ == "__main__":
    # parse argument
    # to get input & output paths & timelimit
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input', help = 'input file path')
    arg_parser.add_argument('output', help = 'output file path')
    arg_parser.add_argument('time_limit', help = 'time limit')
    arg_parser.add_argument('epsilon', help = 'epsilon')
    args = arg_parser.parse_args()
    input_file = args.input
    output_file = args.output
    time_limit = float(args.time_limit)
    epsilon = float(args.epsilon)

    # read input
    with open(input_file, 'r') as fin:
        N = int(fin.readline())
        Sx, Sy = map(int, fin.readline().split())
        Gx, Gy = map(int, fin.readline().split())

        map_mat = [list(map(int, fin.readline().split())) for i in range(N)]

    # heuristic function
    global h
    h = {(x, y): Loo((x, y), (Gx, Gy)) for x, y in itertools.product(range(N), range(N))}

    # run A*
    with open(output_file, "w") as fout:
        request = Request(map_mat, (Sx, Sy), (Gx, Gy), time_limit, epsilon)
        ara_star(request, fout)








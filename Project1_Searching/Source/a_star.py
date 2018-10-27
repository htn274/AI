# run example: python3 a_star_1.py a.in a.out
# for help, run: python3 a_start_1.py --help 
import argparse
import itertools
import queue

INF = 10 ** 9

"""returns the Euclidian distance of (ax, ay) and (bx, by)"""
def Euclide_dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

"""
@mat: input matrix
@S = (Sx, Sy) - Start
@G = (Gx, Gy) - Goal

returns None if Goal is unreacable from Start
otherwise returns the path as a list [(Sx, Sy), (x1, y1), ..., (Gx, Gy)]
"""
def A_star(mat, S, G):
    N = len(mat)

    # node opening order
    DIRs = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]

    # heuristic function
    h = {(x, y): Euclide_dist((x, y), G) for x, y in itertools.product(range(N), range(N))}
    # eh
    g = {S: 0}
    # eh
    pre = {S: S}
    
    # min-priority queue
    pq = queue.PriorityQueue()
    pq.put((h[S], S))

    while pq.qsize():
        f, cur_node = pq.get()
        x, y = cur_node

        for dx, dy in DIRs:
            neighbor_node = (x + dx, y + dy)

            if 0 <= x + dx < N and 0 <= y + dy < N\
                and mat[x + dx][y + dy] != 1\
                and g[cur_node] + 1 < g.get(neighbor_node, INF):
                    g[neighbor_node] = g[cur_node] + 1
                    pq.put((g[neighbor_node] + 1 + h[neighbor_node], neighbor_node))
                    
                    pre[neighbor_node] = cur_node
    
    if G not in pre:
        return None
    path = [G]
    while G != S:
        G = pre[G]
        path.append(G)

    return path[::-1]
    
if __name__ == "__main__":
    # parse argument
    # to get input & output paths
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input', help = 'input file path')
    arg_parser.add_argument('output', help = 'output file path')
    args = arg_parser.parse_args()
    input_file = args.input
    output_file = args.output
    
    # read input
    with open(input_file, 'r') as fin:
        N = int(fin.readline())
        Sx, Sy = map(int, fin.readline().split())
        Gx, Gy = map(int, fin.readline().split())

        map_mat = [list(map(int, fin.readline().split())) for i in range(N)]

    # run A*
    path = A_star(map_mat, (Sx, Sy), (Gx, Gy))

    # write output
    with open(output_file, 'w') as fout:
        if path == None:
            fout.write('-1')
        else:
            fout.write(str(len(path)) + '\n')
            fout.write(' '.join(list(f'({x},{y})' for (x, y) in path)) + '\n')
            for x, y in path:
                if (x, y) not in ((Sx, Sy), (Gx, Gy)):
                    map_mat[x][y] = 'x'

            for x in range(N):
                for y in range(N):
                    if (x, y) == (Sx, Sy):
                        fout.write('S')
                    elif (x, y) == (Gx, Gy):
                        fout.write('G')
                    elif (x, y) in path:
                        fout.write('x')
                    else:
                        fout.write('-' if map_mat[x][y] == 0 else 'o')
                fout.write('\n')

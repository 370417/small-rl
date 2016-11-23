"""
"""

from heapq import heapify, heappop, heappush, heappushpop
from math import inf, ceil

WIDTH = 65
HEIGHT = 24

def astar(startid, endid, neighbors, cost, heuristic):
    """Use the A* algorithm to generate the shortest path between two points

    startid - id of the start node
    endid - id of the end node
    neighbors - a function that takes a node and returns an iterable of that node's neighbors
    cost - a function that takes two nodes returns the cost to move between them
    heuristic - a function that takes a node and returns the estimated distance between it and *start*
    """
    open = {endid: [heuristic(endid), heuristic(endid), 0, endid]}
    closed = {}
    previous = {endid: None}
    openheap = [open[endid]]
    while openheap:
        node = heappop(openheap)
        nodeid = node[3]
        if nodeid == startid:
            while nodeid in previous:
                yield nodeid
                nodeid = previous[nodeid]
            break
        del open[nodeid]
        closed[nodeid] = node
        for neighborid in neighbors(nodeid):
            if not neighborid in closed:
                if neighborid in open:
                    neighbor = open[neighborid]
                else:
                    neighbor = [inf, heuristic(neighborid), inf, neighborid]
                    open[neighborid] = neighbor
                    heappush(openheap, neighbor)
                alt_g = node[2] + cost(nodeid, neighborid)
                if alt_g < neighbor[2]:
                    previous[neighborid] = nodeid
                    neighbor[0] = alt_g + neighbor[1]
                    neighbor[2] = alt_g
                    heapify(openheap)

class Schedule:

    def __init__(self):
        self.schedule = []
        self.time = 0

    def push(self, id, delay):
        heappush(self.schedule, (self.time + delay, id))

    def pop(self):
        time, id = heappop(self.schedule)
        self.time = time
        return id

    def pushpop(self, id, delay):
        time, id = heappushpop(self.schedule, (self.time + delay, id))
        self.time = time
        return id

def shadowcast(cx, cy, transparent):
    def scan(y, start, end, transparent):
        if start < end:
            xmin = round((y - 0.5) * start)
            xmax = ceil((y + 0.5) * end - 0.5)
            for x in range(xmin, xmax + 1):
                if transparent(x, y):
                    if x >= y * start and x <= y * end:
                        yield (x, y)
                        if not transparent(x, y + 1):
                            yield (x, y + 1)
                        if not transparent(x + 1, y + 1):
                            yield (x + 1, y + 1)
                else:
                    yield from scan(y + 1, start, (x - 0.5) / y, transparent)
                    start = (x + 0.5) / y
                    if start >= end:
                        break
            yield from scan(y + 1, start, end, transparent)
    yield (cx, cy)
    transforms = (
        ( 1, 0, 0, 1),
        ( 1, 0, 0,-1),
        (-1, 0, 0, 1),
        (-1, 0, 0,-1),
        ( 0, 1, 1, 0),
        ( 0, 1,-1, 0),
        ( 0,-1, 1, 0),
        ( 0,-1,-1, 0))
    for xx, xy, yx, yy in transforms:
        def transformedtransparent(x, y):
            return transparent(cx + x * xx + y * yx, cy + x * xy + y * yy)
        for x, y in scan(1, 0, 1, transformedtransparent):
            yield (cx + x * xx + y * yx, cy + x * xy + y * yy)

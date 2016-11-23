"""
"""

from heapq import heapify, heappop, heappush, heappushpop
from math import inf, ceil
from collections import namedtuple

WIDTH = 65
HEIGHT = 24

def astar(startid, endid, neighbors, cost, heuristic):
    """Use the A* algorithm to generate the shortest path between two points

    startid - id of the start node
    endid - id of the end node
    neighbors(nodeid) - iterable of the ids of nodeid's neighbor nodes
    cost(previd, nextid) - returns the cost to move between prev and next nodes
    heuristic(nodeid) - returns the estimated distance between node and start
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
    """Represents a schedule of events"""

    def __init__(self):
        self.schedule = []
        self.time = 0

    def push(self, id, delay):
        """Schedule an event with id of id at a time of delay ticks from now"""
        heappush(self.schedule, (self.time + delay, id))

    def pop(self):
        """Get the next event"""
        time, id = heappop(self.schedule)
        self.time = time
        return id

    def pushpop(self, id, delay):
        "Schedule an event with id of id and get the next event"
        time, id = heappushpop(self.schedule, (self.time + delay, id))
        self.time = time
        return id

def scan(y, start, end, transparent):
    """Generate fov for one octant"""
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

def shadowcast(cx, cy, transparent):
    """Generate fov centered on (cx, cy)"""
    yield(cx, cy)
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
        def transform(x, y):
            return (cx + x * xx + y * yx, cy + x * xy + y * yy)
        def transformedtransparent(x, y):
            return transparent(*transform(x, y))
        if not transformedtransparent(0, 1):
            yield transform(0, 1)
        if not transformedtransparent(1, 1):
            yield transform(1, 1)
        for x, y in scan(1, 0, 1, transformedtransparent):
            yield transform(x, y)

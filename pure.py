"""
"""

from heapq import heapify, heappop, heappush, heappushpop
from math import inf

WIDTH = 64
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

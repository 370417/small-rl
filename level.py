"""
"""

import random
from math import inf
from pure import WIDTH, HEIGHT, astar

def generatelevel(seed, startx, starty):
    random.seed(seed)

    tiles = {(x, y): 'wall' for x in range(WIDTH) for y in range(HEIGHT)}
    costs = {(x, y): random.random() for x in range(WIDTH) for y in range(HEIGHT)}

    def place_room(x=None, y=None, width=None, height=None):

        if x == None:
            width = random.randrange(7, 20)
            height = random.randrange(6, 9)
            x = random.randrange(WIDTH - width)
            y = random.randrange(HEIGHT - height)

        for i in range(x, x + width):
            for j in range(y, y + height):
                if tiles[i,j] != 'wall':
                    return False

        for i in range(x + 1, x + width - 1):
            tiles[i,y] = 'hwall'
            tiles[i,y+height-1] = 'hwall'
            for j in range(y + 1, y + height - 1):
                tiles[i,j] = 'floor'
        for j in range(y + 1, y + height - 1):
            tiles[x,j] = 'vwall'
            tiles[x+width-1,j] = 'vwall'
        tiles[x,y] = 'nwcorner'
        tiles[x+width-1,y] = 'necorner'
        tiles[x,y+height-1] = 'swcorner'
        tiles[x+width-1,y+height-1] = 'secorner'

        return {
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'cx': x + width // 2,
            'cy': y + height // 2,
        }

    def place_rooms():
        # place first room
        width = random.randrange(7, 20)
        height = random.randrange(6, 9)
        x = startx - random.randrange(1, width - 1)
        y = starty - random.randrange(1, height - 1)
        rooms = [place_room(x, y, width, height)]

        failures = 0
        successes = 1
        while successes < 5 or failures < 5 * successes:
            room = place_room()
            if room:
                if successes == 1:
                    # place stairs
                    x = room['x'] + random.randrange(2, room['width'] - 2)
                    y = room['y'] + random.randrange(2, room['height'] - 2)
                    tiles[x,y] = 'downstairs'
                successes += 1
                rooms.append(room)
            else:
                failures += 1
        return rooms

    def corridor(x1, y1, x2, y2):

        startid = (x1, y1)
        endid = (x2, y2)

        def neighbors(nodeid):
            x, y = nodeid
            if y > 0:
                yield (x, y - 1)
            if y < HEIGHT - 1:
                yield (x, y + 1)
            if x < WIDTH - 1:
                yield (x + 1, y)
            if x > 0:
                yield (x - 1, y)

        def cost(previd, nextid):
            px, py = previd
            nx, ny = nextid
            prev = tiles[previd]
            next = tiles[nextid]
            if next[2:] == 'corner':
                cost = inf
            elif next in ('floor', 'door', 'corridor', 'downstairs'):
                cost = 1
            elif next == 'wall':
                cost = 2
            elif next == 'wallcorridor' and prev == 'wallcorridor':
                cost = 99
            elif (next[1:] == 'walldoor'
                    or next == 'hwall' and prev == 'hwall' and py == ny
                    or next == 'vwall' and prev == 'vwall' and px == nx):
                cost = 999
            else:
                cost = 4
            return cost + costs[nextid]

        def heuristic(nodeid):
            x, y = nodeid
            return (abs(room1['cx'] - x) + abs(room1['cy'] - y))

        path = astar(startid, endid, neighbors, cost, heuristic)
        for nodeid in path:
            if tiles[nodeid][0:4] == 'wall':
                tiles[nodeid] = 'corridor'
                for neighborid in neighbors(nodeid):
                    if tiles[neighborid] == 'wall':
                        tiles[neighborid] += 'corridor'
            elif tiles[nodeid][1:5] == 'wall':
                tiles[nodeid] = 'door'
                for neighborid in neighbors(nodeid):
                    if tiles[neighborid][1:] == 'wall':
                        tiles[neighborid] += 'door'

    def randtile():
        x = random.randrange(WIDTH)
        y = random.randrange(HEIGHT)
        if tiles[x,y] in ('floor', 'corridor'):
            return (x, y)
        else:
            return randtile()

    rooms = place_rooms()

    for i in range(len(rooms) - 1):
        room1 = rooms[i]
        room2 = rooms[i+1]
        corridor(room1['cx'], room1['cy'], room2['cx'], room2['cy'])

    for room in rooms:
        x1, y1 = randtile()
        x2, y2 = randtile()
        corridor(x1, y1, x2, y2)

    return tiles

class Level:
    """A map level"""

    def __init__(self, seed, x, y):
        self.tiles = generatelevel(seed, x, y)
        self.actors = {}
        self.deathpath = {}

    def transparent(self, x, y):
        if (x, y) in self.tiles:
            return self.tiles[x,y] in ('floor', 'corridor', 'downstairs', 'upstairs')
        else:
            return False


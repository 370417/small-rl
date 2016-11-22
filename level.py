"""
"""

import random
from math import inf
from pure import WIDTH, HEIGHT, astar

def generatelevel(seed):
    random.seed(seed)

    types = {(x, y): 'wall' for x in range(WIDTH) for y in range(HEIGHT)}

    def place_room():
        width = random.randrange(7, 20)
        height = random.randrange(6, 9)
        x = random.randrange(WIDTH - width)
        y = random.randrange(HEIGHT - height)

        for i in range(x, x + width):
            for j in range(y, y + height):
                if types[i,j] != 'wall':
                    return False

        for i in range(x + 1, x + width - 1):
            types[i,y] = 'hwall'
            types[i,y+height-1] = 'hwall'
            for j in range(y + 1, y + height - 1):
                types[i,j] = 'floor'
        for j in range(y + 1, y + height - 1):
            types[x,j] = 'vwall'
            types[x+width-1,j] = 'vwall'
        types[x,y] = 'nwcorner'
        types[x+width-1,y] = 'necorner'
        types[x,y+height-1] = 'swcorner'
        types[x+width-1,y+height-1] = 'secorner'

        return {
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'cx': x + width // 2,
            'cy': y + height // 2,
        }

    def place_rooms():
        failures = 0
        successes = 0
        rooms = []
        while successes < 5 or failures < 5 * successes:
            room = place_room()
            if room:
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
            prev = types[previd]
            next = types[nextid]
            if next[2:] == 'corner':
                return inf
            elif next in ('floor', 'door', 'corridor', 'floorsafe'):
                return 1
            elif next == 'wall':
                return 2
            elif next == 'wallcorridor' and prev == 'wallcorridor':
                return 99
            elif (next[1:] == 'walldoor'
                    or next == 'hwall' and prev == 'hwall' and py == ny
                    or next == 'vwall' and prev == 'vwall' and px == nx):
                return 999
            else:
                return 4

        def heuristic(nodeid):
            x, y = nodeid
            return (abs(room1['cx'] - x) + abs(room1['cy'] - y))

        path = astar(startid, endid, neighbors, cost, heuristic)
        for nodeid in path:
            if types[nodeid][0:4] == 'wall':
                types[nodeid] = 'corridor'
                for neighborid in neighbors(nodeid):
                    if types[neighborid] == 'wall':
                        types[neighborid] += 'corridor'
            elif types[nodeid][1:5] == 'wall':
                types[nodeid] = 'door'
                for neighborid in neighbors(nodeid):
                    if types[neighborid][1:] == 'wall':
                        types[neighborid] += 'door'
            elif types[nodeid] == 'floor':
                types[nodeid] = 'floorsafe'

    def randtile():
        x = random.randrange(WIDTH)
        y = random.randrange(HEIGHT)
        if types[x,y] in ('floor', 'corridor'):
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

    return types

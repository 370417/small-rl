"""
"""

import random
from math import inf
from pure import WIDTH, HEIGHT, Schedule
from level import Level
import actor

def creategame(output, input):
    seed = random.randrange(9999)
    #seed = 9847
    print(seed)

    player = actor.Player(
        input = input,
        output = output, 
        x = 33,
        y = 13,
        level = None)

    level = Level(seed, player.x, player.y)

    player.movelevel(level)

    #for x in range(WIDTH):
    #    for y in range(HEIGHT):
    #        output(('put', x, y, char[level.tiles[x,y]]))

    schedule = Schedule()

    player.act(schedule)

    #output(('done',))
    #next(input)

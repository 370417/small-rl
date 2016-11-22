"""
"""

import random
from math import inf
from pure import WIDTH, HEIGHT, Schedule
from level import generatelevel
import actor

char = {
    'wall': 0x20,
    'floor': 0x2E,
    'floorsafe': 0x2C,
    'hwall': 0x2500,
    'vwall': 0x2502,
    'hwalldoor': 0x2500,
    'vwalldoor': 0x2502,
    'nwcorner': 0x250C,
    'necorner': 0x2510,
    'swcorner': 0x2514,
    'secorner': 0x2518,
    'corridor': 0x23,
    'door': 0x2B,
    'wallcorridor': 0x20,
}

def creategame(output, input):
    seed = random.randrange(9999)
    #seed = 9847
    print(seed)

    types = generatelevel(seed)

    for x in range(WIDTH):
        for y in range(HEIGHT):
            output(('put', x, y, char[types[x,y]]))

    schedule = Schedule()

    player = actor.Player(input, output)
    player.act(schedule)

    #output(('done',))
    #next(input)

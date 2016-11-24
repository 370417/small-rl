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
        position = (33, 13),
        level = None)

    level = Level(seed, *player.position)

    reaper = actor.Reaper(
        position = player.position,
        level = level)

    player.movelevel(level)

    schedule = Schedule()
    schedule.push(reaper.id, 120)

    player.act(schedule)

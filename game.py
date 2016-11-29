"""
"""

import random
from math import inf
from pure import WIDTH, HEIGHT, Schedule
from level import Level
import actor

def creategame(output, input):
    seed = random.randrange(9999)
    print(seed)

    player = actor.Player(
        input = input,
        output = output,
        position = (33, 13),
        level = None,
        fovrange = inf,
    )

    level = Level(seed, *player.position)

    reaper = actor.Reaper(
        position = player.position,
        level = level)

    player.movelevel(level)

    schedule = Schedule()
    schedule.push(player.id, 0)
    schedule.push(reaper.id, 18)

    currentactor = actor.Actor.actors[schedule.pop()]
    while schedule.peek():
        delay = currentactor.act()
        if delay < 0:
            break
        currentactor = actor.Actor.actors[schedule.pushpop(currentactor.id, delay)]

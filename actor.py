"""
"""

class Actor:
    """An actor is an object that has an act function and can be scheduled"""

    actors = {}
    newactorid = 0

    def __init__(self):
        self.state = ''
        self.behaviors = {}
        self.id = Actor.newactorid

        Actor.newactorid += 1
        Actor.actors[self.id] = self

    def act(self, schedule):
        delay = self.behaviors[self.state]()
        nextactorid = schedule.pushpop(self.id, delay)
        actors[nextactorid].act(schedule)

class Mover(Actor):
    """An actor that can move around the map"""

    def __init__(self, x, y, level, **kwargs):
        super().__init__(**kwargs)
        self.x = x
        self.y = y
        self.level = level

    def move(self, dx, dy):
        return 12

class Player(Mover):
    """A player is an actor who can give and receive input and output"""

    def __init__(self, input, output, **kwargs):
        super().__init__(**kwargs)
        self.input = input
        self.output = output

    def act(self, schedule):
        self.output(('done',))
        input = next(self.input)
        inputtype = input[0]
        inputargs = input[1:]
        if inputtype == 'quit':
            return
        actions = {'move': self.move}
        delay = actions[inputtype](*inputargs)
        nextactorid = schedule.pushpop(self.id, delay)
        Actor.actors[nextactorid].act(schedule)

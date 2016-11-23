"""
"""

from pure import shadowcast

class Actor:
    """An actor is an object that has an act function and can be scheduled"""

    actors = {}
    newactorid = 0

    def __init__(self):
        self.state = ''
        self.behaviors = {}
        self.id = Actor.newactorid
        self.delay = 12
        self.char = '?'

        Actor.newactorid += 1
        Actor.actors[self.id] = self

    def act(self, schedule):
        delay = self.behaviors[self.state]()
        nextactorid = schedule.pushpop(self.id, delay)
        actors[nextactorid].act(schedule)

class Mover(Actor):
    """An actor that can move around the level"""

    def __init__(self, position, level, **kwargs):
        super().__init__(**kwargs)
        self.position = position
        self.level = level

    def move(self, dx, dy):
        x, y = self.position
        target = (x + dx, y + dy)
        self.level.actors.pop(self.position)
        self.position = target
        self.level.actors[self.position] = self
        return self.delay

    def movelevel(self, level):
        self.level = level
        if self.position in level.actors:
            print('movelevel: target is occupied')
        else:
            level.actors[self.position] = self
        return self.delay

class Player(Mover):
    """A player is an actor who can give and receive input and output"""

    def __init__(self, input, output, **kwargs):
        super().__init__(**kwargs)
        self.input = input
        self.output = output
        self.char = '@'

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

    def move(self, dx, dy):
        delay = super().move(dx, dy)
        self.see()
        return delay

    def movelevel(self, level):
        delay = super().movelevel(level)
        self.see()
        return delay

    def see(self):
        #for position, tile in self.level.tiles.items():
        #    self.output(('put', *position, tile))
        for position in shadowcast(*self.position, self.level.transparent):
            self.output(('put', *position, self.level.tiles[position]))
            if (position in self.level.actors):
                self.output(('put', *position, self.level.actors[position].char))

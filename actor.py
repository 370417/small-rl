"""
"""

from pure import shadowcast

class Actor:
    """An actor is an object that has an act function and can be scheduled"""

    actors = {}
    newactorid = 1

    def __init__(self):
        self.id = Actor.newactorid
        self.delay = 2
        self.char = '?'

        Actor.newactorid += 1
        Actor.actors[self.id] = self

    def act(self):
        return self.delay

class Event(Actor):
    """An actor that calls a function once then removes itself"""

    def __init__(self, function, **kwargs):
        super().__init__(**kwargs)
        self.function = function

    def act(self, schedule):
        del Actor.actors[self.id]
        self.function()
        Actor.actors[schedule.pop()].act(schedule)

class Mover(Actor):
    """An actor that can move around the level"""

    def __init__(self, position, level, **kwargs):
        super().__init__(**kwargs)
        self.position = position
        self.level = level

    def canmove(self, dx, dy, level=None):
        if not level:
            level = self.level
        x, y = self.position
        return level.tiles[x+dx,y+dy] in ('floor', 'door', 'corridor')

    def move(self, dx, dy):
        x, y = self.position
        target = (x + dx, y + dy)
        self.level.actors.pop(self.position)
        self.position = target
        self.level.actors[self.position] = self

    def movelevel(self, level):
        self.level = level
        if self.position in level.actors:
            print('movelevel: target is occupied')
        else:
            level.actors[self.position] = self

class Seer(Mover):
    """An actor that can see"""

    def __init__(self, fovrange, **kwargs):
        super().__init__(**kwargs)
        self.fovrange = fovrange
        self.visible = set()

    def look(self):
        self.visible = set(shadowcast(*self.position, self.level.transparent))

    def see(self, sight):
        pass

class Player(Seer):
    """A player is an actor who can give and receive input and output"""

    def __init__(self, input, output, **kwargs):
        super().__init__(**kwargs)
        self.input = input
        self.output = output
        self.char = '@'
        self.fov = {}
        self.seen = set()

    def act(self):
        for position in self.visible:
            if position in self.level.actors:
                actor = self.level.actors[position]
            else:
                actor = None
            if position in self.level.deathpath:
                deathpath = self.level.deathpath[position]
            else:
                deathpath = None
            self.output((
                'see',
                *position,
                self.level.tiles[position],
                deathpath,
                actor))
        for x, y in self.oldvisible - self.visible:
            self.output(('unsee', x, y))
        self.output(('done',))
        input = next(self.input)
        inputtype = input[0]
        inputargs = input[1:]
        if inputtype == 'quit':
            return -1
        actions = {'move': self.move}
        successful = actions[inputtype](*inputargs)
        if successful:
            return super().act()
        else:
            return self.act()

    def move(self, dx, dy):
        if self.canmove(dx, dy):
            self.level.deathpath[self.position] = (dx, dy)
            super().move(dx, dy)
            self.look()
            return True
        else:
            return False

    def movelevel(self, level):
        super().movelevel(level)
        self.look()

    def look(self):
        self.oldvisible = self.visible
        super().look()

class Reaper(Mover):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.char = 'R'
        self.spawned = False

    def act(self):
        if self.spawned:
            direction = self.level.deathpath[self.position]
            del self.level.deathpath[self.position]
            self.move(*direction)
        else:
            self.movelevel(self.level)
            self.spawned = True
        return super().act()

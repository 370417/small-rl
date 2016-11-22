"""
"""

class Actor:
    """An actor is an object that has an act function and can be scheduled"""

    actors = {}
    newactorid = 0

    def __init__(self):
        self.state = ''
        self.behaviors = {}
        self.id = newactorid

        newactorid += 1
        actors[self.id] = self

    def act(self, schedulepushpop):
        delay = self.behaviors[self.state]()
        nextactorid = schedulepushpop(self.id, delay)
        actors[nextactorid].act(schedulepushpop)

class Player(Actor):
    """"""

    def __init__(self, input):
        super().__init__(self)
        self.input = input

    def act(self, schedulepushpop):
        input = next(self.input)
        # execute action and find delay
        delay = 0
        nextactorid = schedulepushpop(self.id, delay)
        actors[nextactorid].act(schedulepushpop)

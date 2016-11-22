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

class Player(Actor):
    """A player is an actor who can give and receive input and output"""

    def __init__(self, input, output):
        super().__init__()
        self.input = input
        self.output = output

    def act(self, schedule):
        self.output(('done',))
        input = next(self.input)
        # execute action and find delay
        delay = 0
        nextactorid = schedule.pushpop(self.id, delay)
        Actor.actors[nextactorid].act(schedule)

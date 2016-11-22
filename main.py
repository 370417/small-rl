"""
"""

from bearlibterminal import terminal as blt
from game import creategame

def read():
    while True:
        yield blt.read()

blt.open()
blt.set('window.title="smallrl"')

def gameoutput(output):
    type = output[0]
    if type == 'put':
        x, y, char = output[1:]
        blt.put(x, y, char)
    elif type == 'done':
        blt.refresh()

def gameinput():
    for key in read():
        if key == blt.TK_Q and blt.check(blt.TK_SHIFT):
            blt.close()
            break
    yield 'wawawawa'

creategame(gameoutput, gameinput())

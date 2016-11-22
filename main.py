"""
"""

from bearlibterminal import terminal as blt
from game import creategame

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

def read():
    while True:
        yield blt.read()

blt.open()
blt.set('window.title="smallrl"')

def gameoutput(output):
    type = output[0]
    if type == 'put':
        x, y, tile = output[1:]
        blt.put(x, y, char[tile])
    elif type == 'done':
        blt.refresh()

def gameinput():
    for key in read():
        if key == blt.TK_Q and blt.check(blt.TK_SHIFT):
            blt.close()
            break
        elif key == blt.TK_UP or key == blt.TK_K:
            yield ('move', 0, -1)
        elif key == blt.TK_DOWN or key == blt.TK_J:
            yield ('move', 0, 1)
        elif key == blt.TK_LEFT or key == blt.TK_H:
            yield ('move', -1, 0)
        elif key == blt.TK_RIGHT or key == blt.TK_L:
            yield ('move', 1, 0)
    yield ('quit',)

creategame(gameoutput, gameinput())

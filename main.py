"""
"""

from bearlibterminal import terminal as blt
from game import creategame

char = {
    'wall': ' ',
    'floor': '.',
    'hwall': '─',
    'vwall': '│',
    'hwalldoor': '─',
    'vwalldoor': '│',
    'nwcorner': '┌',
    'necorner': '┐',
    'swcorner': '└',
    'secorner': '┘',
    'corridor': '#',
    'door': '+',
    'wallcorridor': ' ',
    ( 1, 0): '→',
    (-1, 0): '←',
    ( 0,-1): '↑',
    ( 0, 1): '↓',
}

def read():
    while True:
        yield blt.read()

blt.open()
blt.set('window.title="smallrl"')

tiles = {}

def gameoutput(output):
    type = output[0]
    if type == 'see':
        blt.color('white')
        x, y, tile, deathpath, actor = output[1:]
        tiles[x,y] = char[tile]
        if actor:
            blt.put(x, y, actor.char)
        elif deathpath:
            blt.put(x, y, char[deathpath])
        else:
            blt.put(x, y, tiles[x,y])
    elif type == 'unsee':
        blt.color('gray')
        x, y = output[1:]
        blt.put(x, y, tiles[x,y])
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

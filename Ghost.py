from enum import Enum
from GameThing import GameThing
from Wall import Wall

class GhostName(Enum):
    Blinky = 'Blinky'
    Pinky = 'Pinky'
    Inky = 'Inky'
    Clyde = 'Clyde'

class GhostMovementMode(Enum):
    Chase = 0
    Scatter = 1
    Frightened = 2

# (X, Y)
ScatterTargets = {
    'Blinky': (0, -3),
    'Pinky': (0, 3),
    'Inky': (-1, -1),
    'Clyde': (0, -1)
}

class Ghost(GameThing):
    _char_ = '# '

    ghosts = {}

# [14][13], [14][16], [26][13], [26][16]
    def __init__(self, gamemap, x, y, pacman, name):
        GameThing.__init__(self, gamemap, x, y)
        self.pacman = pacman
        self.name = name
        self.ghosts[name] = self
        self.mode = GhostMovementMode.Scatter
        self.scatterTarget = self._get_scatter_target_(self.name)
        self.target = self.scatterTarget
        self.lastPos = (-1, -1)
        self.onTopOf = None
        # raise Exception(str(self.scatterTarget))

    def _get_scatter_target_(self, name):
        if name is GhostName.Blinky: return (len(self.gamemap[0]) - 3, 0)
        elif name is GhostName.Pinky: return (3, 0)
        elif name is GhostName.Inky: return (len(self.gamemap[0]), len(self.gamemap))
        elif name is GhostName.Clyde: return (len(self.gamemap), 0)

    def change_mode(self, mode):
        # TODO: reverse direction
        self.mode = mode

    def _get_next_tile_(self):
        if self.mode is GhostMovementMode.Scatter:
            self.target = self.scatterTarget
        else:
            self.target = (self.pacman.x, self.pacman.y)
        # Ignore positions that are walls.
        # This position is important, because we want up > left > down > right if there are more than one possible,
        # equidistant options. Items lower on the list will override higher ones, so this works.
        possible_pos = filter(lambda pos: not isinstance(self.gamemap[pos[1]][pos[0]], Wall), [
            (self.x + 1, self.y),  # Right
            (self.x, self.y + 1),  # Down
            (self.x - 1, self.y),  # Left
            (self.x, self.y - 1),  # Up
        ])

        min_distance = None
        next_square = None
        for pos in possible_pos:
            # At four positions, the ghost can't go up
            if pos in ((13, 14), (16, 14), (13, 26), (16, 26)) and pos[1] > self.y: continue
            x, y = pos
            tx, ty = self.target
            # Don't
            if self.lastPos[0] is x and self.lastPos[1] is y: continue
            distance = (x - tx) ** 2 + (y - ty) ** 2 # This is the `a^2 + b^2` part of the pythagorean theorem.
            if not min_distance or min_distance > distance: min_distance, next_square = distance, pos

        x, y = next_square
        self.lastPos = (self.x, self.y)
        self.gamemap[self.y][self.x] = self.onTopOf
        self.onTopOf = self.gamemap[y][x]
        self.gamemap[y][x] = self
        self.x, self.y = x, y

    def get_next_move(self):
        self._get_next_tile_()


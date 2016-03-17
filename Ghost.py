from enum import Enum
from random import choice
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


class Ghost(GameThing):
    _char_ = '# '

    ghosts = {}

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
        if name is GhostName.Blinky:
            return (len(self.gamemap[0]) - 3, 0)
        elif name is GhostName.Pinky:
            return (3, 0)
        elif name is GhostName.Inky:
            return (len(self.gamemap[0]), len(self.gamemap))
        elif name is GhostName.Clyde:
            return (len(self.gamemap), 0)

    def change_mode(self, mode):
        # TODO: reverse direction
        self.mode = mode

    def _get_next_tile_(self):
        # Ignore positions that are walls.
        # This position is important, because we want up > left > down > right if there are more than one possible,
        # equidistant options. Items lower on the list will override higher ones, so this works.
        is_valid_pos = lambda pos: not (pos[0] is self.lastPos[0] and pos[1] is self.lastPos[1]) and \
                                   not isinstance(self.gamemap[pos[1]][pos[0]], Wall)
        possible_pos = list(filter(is_valid_pos, [
            (self.x + 1, self.y),  # Right
            (self.x, self.y + 1),  # Down
            (self.x - 1, self.y),  # Left
            (self.x, self.y - 1),  # Up
        ]))

        next_square = None
        if self.mode is GhostMovementMode.Frightened:
            next_square = choice(possible_pos)
        elif self.mode in (GhostMovementMode.Scatter, GhostMovementMode.Chase):
            min_distance = None
            self.target = \
                self.scatterTarget if self.mode is GhostMovementMode.Scatter else (self.pacman.x, self.pacman.y)

            for pos in possible_pos:
                # At four positions, the ghost can't go up
                if pos in ((13, 13), (16, 13), (13, 25), (16, 25)) and pos[1] > self.y: continue
                x, y = pos
                tx, ty = self.target
                # Don't
                if self.lastPos[0] is x and self.lastPos[1] is y: continue
                distance = (x - tx) ** 2 + (y - ty) ** 2  # This is the `a^2 + b^2` part of the pythagorean theorem.
                if not min_distance or min_distance > distance: min_distance, next_square = distance, pos

        x, y = next_square

        if y is 14 and x > 27:  # Right Portal
            x = 0
        elif y is 14 and x < 0:  # Left Portal
            x = 27

        self.lastPos = (self.x, self.y)
        self.gamemap[self.y][self.x] = self.onTopOf
        self.onTopOf = self.gamemap[y][x]
        self.gamemap[y][x] = self
        self.x, self.y = x, y

    def get_next_move(self):
        self._get_next_tile_()

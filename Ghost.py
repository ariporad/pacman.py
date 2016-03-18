from enum import Enum
from random import choice
from GameThing import GameThing
from Wall import Wall
from utils import direction


class GhostManager:
    blinky = None
    pinky = None
    inky = None
    clyde = None


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
    """
    A base class for Ghosts. You shouldn't use it directly, but rather subclass it. Subclasses should impliment the
    following methods/properties:
    - __init__:
        - Must set self.scatterTarget to something based off the height and width of the game board.
        - Must set self.manager.<ghost name> to self.
    - _get_target_square_:
        - Must return the current target square. This is usually based off pacman's position. Should return (x, y).
          *THIS WILL ONLY BE CALLED DURING CHASE MODE. DURING SCATTER self.scatterTarget IS USED, AND EVERYTHING IS
          RANDOM IN FRIGHTENED.*
    - self.name: the name of the ghost (ex. 'Blinky')
    """
    _char_ = '# '
    scatterTarget = 0, 0

    def __init__(self, manager, gamemap, x, y, pacman):
        GameThing.__init__(self, gamemap, x, y)
        self.manager = manager
        self.pacman = pacman
        self.mode = GhostMovementMode.Scatter
        self.target = self.scatterTarget
        self.lastPos = (-1, -1)
        self.onTopOf = None

    # def _get_scatter_target_(self, name):
    #     if name is GhostName.Blinky:
    #         return (len(self.gamemap[0]) - 3, 0)
    #     elif name is GhostName.Pinky:
    #         return
    #     elif name is GhostName.Inky:
    #         return (len(self.gamemap[0]), len(self.gamemap))
    #     elif name is GhostName.Clyde:
    #         return (len(self.gamemap), 0)

    def change_mode(self, mode):
        # TODO: reverse direction
        self.mode = mode

    def _get_target_square_(self):
        return self.scatterTarget

    def get_next_move(self):
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
            min_distance = 0
            self.target = self.scatterTarget if self.mode is GhostMovementMode.Scatter else self._get_target_square_()

            if self.gamemap[self.target[1]][self.target[0]]:
                self.gamemap[self.target[1]][self.target[0]].render = lambda: '!'

            for pos in possible_pos:
                # At four positions, the ghost can't go up
                if pos in ((12, 13), (15, 13), (12, 25), (15, 25)) and pos[1] < self.y: continue
                x, y = pos
                tx, ty = self.target or (-1, -1)
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


class Blinky(Ghost):
    name = 'Blinky'

    def __init__(self, manager, gamemap, x, y, pacman):
        Ghost.__init__(self, manager, gamemap, x, y, pacman)
        self.scatterTarget = (len(self.gamemap[0]) - 3, 0)
        self.manager.blinky = self

    def _get_target_square_(self):
        return self.pacman.x, self.pacman.y


class Pinky(Ghost):
    name = 'Pinky'
    scatterTarget = 3, 0

    def __init__(self, manager, gamemap, x, y, pacman):
        Ghost.__init__(self, manager, gamemap, x, y, pacman)
        self.manager.blinky = self

    def _get_target_square_(self):
        pacman_direction = direction(self.pacman.oldX, self.pacman.oldY, self.pacman.x, self.pacman.y)
        if pacman_direction is 1:  # down
            return self.pacman.x, self.pacman.y + 4
        elif pacman_direction is 2:  # left
            return self.pacman.x - 4, self.pacman.y
        elif pacman_direction is 3:  # right
            return self.pacman.x + 4, self.pacman.y
        elif pacman_direction is 0:  # up, Special Case.
            return self.pacman.x - 4, self.pacman.y - 4
        else:
            return self.target

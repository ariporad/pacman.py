from CONSTANTS import *
from Pacman import Pacman
from Wall import Wall, WallType
from Pellet import Pellet

class MapError(Exception):
    pass

class MapReader:
    def read(self, file):
        gamemap = [([None] * WIDTH) for _ in range(HEIGHT)]
        pacman = None
        #ghosts = []
        with open(file) as f:
            for y, line in enumerate(f):
                chars = list(line.rstrip('\n'))
                for x, char in enumerate(chars):
                    if char is '@':
                        if pacman: raise MapError('Duplicate Pacman!')
                        pacman = Pacman(x, y)
                        gamemap[y][x] = pacman
                    elif char in WALLS:
                        gamemap[y][x] = Wall(x, y, WallType(char))
                    elif char is PELLET:
                        gamemap[y][x] = Pellet(x, y)
        return (gamemap, pacman)


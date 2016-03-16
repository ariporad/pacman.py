from CONSTANTS import *
from Pacman import Pacman
from Wall import Wall, WallType
from Pellet import Pellet
from Ghost import Ghost, GhostName

class MapError(Exception):
    pass

class MapReader:
    def read(self, file):
        gamemap = [([None] * WIDTH) for _ in range(HEIGHT)]
        pacman = None
        ghosts = []
        with open(file) as f:
            pellets = 0
            for y, line in enumerate(f):
                chars = list(line.rstrip('\n'))
                for x, char in enumerate(chars):
                    if char is '@':
                        if pacman: raise MapError('Duplicate Pacman!')
                        pacman = Pacman(gamemap, x, y)
                        gamemap[y][x] = pacman
                    elif char is 'B':
                        ghosts.append((x, y, GhostName.Blinky))
                    elif char in WALLS:
                        gamemap[y][x] = Wall(gamemap, x, y, WallType(char))
                    elif char is PELLET:
                        pellets += 1
                        gamemap[y][x] = Pellet(gamemap, x, y)
            # We instantiate all the ghosts here so that they have a pacman
            ghosts = list(map(lambda pos: Ghost(gamemap, pos[0], pos[1], pacman, pos[2]), ghosts))
        # raise MapError('Pellets: ' + str(pellets))
        return (gamemap, pacman, ghosts)


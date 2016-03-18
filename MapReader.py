from CONSTANTS import *
from Pacman import Pacman
from Wall import Wall, WallType
from Pellet import Pellet
from Ghost import Ghost, GhostName, GhostManager, Blinky, Pinky

class MapError(Exception):
    pass

class MapReader:
    def read(self, file):
        gamemap = [([None] * WIDTH) for _ in range(HEIGHT)]
        pacman = None
        ghostManager = GhostManager()
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
                        ghosts.append((x, y, Blinky))
                    elif char is 'P':
                        ghosts.append((x, y, Pinky))
                    elif char in WALLS:
                        gamemap[y][x] = Wall(gamemap, x, y, WallType(char))
                    elif char is PELLET:
                        pellets += 1
                        gamemap[y][x] = Pellet(gamemap, x, y)
            # We instantiate all the ghosts here so that they have a pacman
            ghosts = list(map(lambda pos: pos[2](ghostManager, gamemap, pos[0], pos[1], pacman), ghosts))
        return (gamemap, pacman, ghosts, ghostManager)


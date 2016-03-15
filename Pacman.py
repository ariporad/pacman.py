from GameThing import GameThing
from Wall import Wall
from Pellet import Pellet

class Pacman(GameThing):
    def __init__(self, x, y):
        GameThing.__init__(self, x, y)
        self.points = 0

    # +X = right, +Y = down
    def move(self, gamemap, X = 0, Y = 0): # TODO: don't take a gamemap
        newX, newY = self.x + X, self.y + Y
        if isinstance(gamemap[newY][newX], Wall):
            return # Can't move into a wall
        elif isinstance(gamemap[newY][newX], Pellet):
            self.points += 1
        elif newY is 14 and newX > 27:  # Right Portal
            newX = 0
        elif newY is 14 and newX < 0:  # Left Portal
            newX = 27
        gamemap[self.y][self.x] = None
        gamemap[newY][newX] = self
        self.x, self.y = newX, newY

    def render(self):
        return 'ᗤ' # TODO: Change direction of glyph based off direction of movement
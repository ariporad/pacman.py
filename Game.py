from Renderer import Renderer
from getch import getch
from sys import exit

class Game:
    def __init__(self, gamemap, pacman):
        self.gamemap, self.pacman = gamemap, pacman
        self.r = Renderer()

    def start(self):
        while True:
            self.r.draw(self.gamemap)
            key = getch()
            if key is 'q':
                exit(0)
            elif key is '\033':
                key = getch()
                if key is '[':
                    key = getch()
                    if key is 'A':
                        self.pacman.move(self.gamemap, Y=-1)
                    elif key is 'B':
                        self.pacman.move(self.gamemap, Y=1)
                    elif key is 'C':
                        self.pacman.move(self.gamemap, X=1)
                    elif key is 'D':
                        self.pacman.move(self.gamemap, X=-1)


from Renderer import Renderer
from readchar import readkey
from sys import exit
from time import sleep
from threading import Thread


class GameSubthread(Thread):
    daemon = True
    def __init__(self, g):
        Thread.__init__(self)
        self.g = g

    def run(self):
        self.g._input_thread_()


class Game:
    def __init__(self, gamemap, pacman, ghosts):
        self.gamemap, self.pacman, self.ghosts = gamemap, pacman, ghosts
        self.r = Renderer()
        self._should_exit_ = False

    def _input_thread_(self):
        while True:
            key = readkey()
            if key is 'q':
                self._should_exit_ = True
            elif key is 'w':
                self.pacman.move(Y=-1)
            elif key is 'a':
                self.pacman.move(X=-1)
            elif key is 's':
                self.pacman.move(Y=1)
            elif key is 'd':
                self.pacman.move(X=1)

    def start(self):
        subthread = GameSubthread(self)
        subthread.start()
        while True:
            if self._should_exit_: return exit(0)
            for ghost in self.ghosts: ghost.get_next_move()
            self.r.draw(self.gamemap)
            sleep(0.1)

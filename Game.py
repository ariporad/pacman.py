from Renderer import Renderer
from readchar import readkey
from time import sleep
from threading import Thread
from Ghost import GhostMovementMode


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
            elif key is 'c':
                for ghost in self.ghosts: ghost.change_mode(GhostMovementMode.Chase)
            elif key is 'x':
                for ghost in self.ghosts: ghost.change_mode(GhostMovementMode.Scatter)
            elif key is 'f':
                for ghost in self.ghosts: ghost.change_mode(GhostMovementMode.Frightened)
            elif key is 'w':
                self.pacman.move(Y=-1)
            elif key is 'a':
                self.pacman.move(X=-1)
            elif key is 's':
                self.pacman.move(Y=1)
            elif key is 'd':
                self.pacman.move(X=1)

    def _cleanup_(self):
        print('\n\r', end='')

    def start(self):
        subthread = GameSubthread(self)
        subthread.start()
        while True:
            if self._should_exit_:
                self._cleanup_()
                return
            for ghost in self.ghosts: ghost.get_next_move()
            self.r.draw(self.gamemap)
            sleep(0.1)

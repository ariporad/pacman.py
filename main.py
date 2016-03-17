from MapReader import MapReader
from Game import Game
import termios


def main():
    stdin_attrs = termios.tcgetattr(0)
    stdout_attrs = termios.tcgetattr(1)
    stderr_attrs = termios.tcgetattr(2)

    try:
        reader = MapReader()
        gamemap, pacman, ghosts = reader.read('gamemap.txt')
        g = Game(gamemap, pacman, ghosts)
        g.start()
    finally:
        termios.tcsetattr(0, termios.TCSANOW, stdin_attrs)
        termios.tcsetattr(1, termios.TCSANOW, stdout_attrs)
        termios.tcsetattr(2, termios.TCSANOW, stderr_attrs)


if __name__ == '__main__':
    main()


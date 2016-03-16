from MapReader import MapReader
from Game import Game


def main():
    reader = MapReader()
    gamemap, pacman, ghosts = reader.read('gamemap.txt')
    g = Game(gamemap, pacman, ghosts)
    g.start()


if __name__ == '__main__':
    main()


from enum import Enum
from GameThing import GameThing

class WallType(Enum):
    """
    An enum for the various types of Wall(s).
    """
    vertical = '┃'
    horizontal = '━'
    corner_top_left = '┏'
    corner_top_right = '┓'
    corner_bottom_left = '┗'
    corner_bottom_right = '┛'
    t = '┳'


class Wall(GameThing):
    """
    A wall on the game map. Currently just a container which knows it's position and how to render.
    """
    def __init__(self, x, y, type):
        GameThing.__init__(self, x, y)
        if not isinstance(type, WallType): raise TypeError('Must pass a WallType to Wall')
        self.type = type

    def render(self):
        if self.type in (WallType.vertical, WallType.corner_top_right, WallType.corner_bottom_right):
            return self.type.value + ' '
        else:
            return self.type.value + WallType.horizontal.value
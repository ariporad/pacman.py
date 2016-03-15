class GameThing:
    """
    A generic base class for anything on the game board
    """

    def __init__(self, gamemap, x, y):
        """
        :param x: The (initial) x coordinate of the object
        :param y: The (initial) y coordinate of the object
        :return: None
        """
        self.x, self.y, self.gamemap = x, y, gamemap

    def __str__(self):
        return self.render()

    _char_ = '  '
    def render(self): # In the future, this might take some sort of state
        """
        :return: A str, with a length of two, which is how the object should be rendered.
        """
        return self._char_
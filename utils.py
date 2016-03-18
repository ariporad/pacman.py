import math


def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


def direction(oldX, oldY, newX, newY):
    """
    Determine the direction something is moving from its current and past coordinates. Does not support diagonals.
    :param oldX: Old X Position
    :param oldY: Old Y Position
    :param newX: New X Position
    :param newY: New Y Position
    :return: 0 = up, 1 = down, 2 = left, 3 = right
    """
    diffX = sign(newX - oldX)
    diffY = sign(newY - oldY)

    # print('diffX: {!s}, diffY: {!s}'.format(diffX, diffY))
    if diffY is -1:
        return 0
    elif diffY is 1:
        return 1
    elif diffX is -1:
        return 2
    elif diffX is 1:
        return 3

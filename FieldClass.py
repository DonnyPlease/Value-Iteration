class Element:
    """
    Class describing one element in the grid of the field.
    """
    def __init__(self):
        self.__reward = 0
        self.__isAbsorber = False
        self.__isWall = False
        self.__bestDirection = 0  # clockwise nomenclature, north = 0, east = 1, south = 2, west = 3

    def setAbsorber(self, reward):
        self.__isAbsorber = True
        self.__reward = reward

    def unsetAbsorber(self):
        self.__isAbsorber = False

    def setWall(self):
        self.__isWall = True

    def unsetWall(self):
        self.__isWall = False

    def getReward(self):
        return self.__reward

    def setReward(self, newReward):
        self.__reward = newReward

    def isWall(self):
        return self.__isWall

    def isAbsorber(self):
        return self.__isAbsorber

    def getBestDirection(self):
        return self.__bestDirection

    def setBestDirection(self, bestDirection):
        self.__bestDirection = bestDirection


class Field:
    """Class representing grid of cell (type Element)."""

    def __init__(self, rows=3, columns=4):
        self.__field = []
        self.__height = rows
        self.__width = columns

        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(Element())
            self.__field.append(row)

    def getRowsAndCols(self):
        return self.__height, self.__width

    def setAbsorber(self, col, row, reward=100):
        self.__field[row][col].setAbsorber(reward)

    def unsetAbsorber(self, col, row):
        self.__field[row][col].unsetAbsorber()

    def setWall(self, col, row):
        self.__field[row][col].setWall()

    def unsetWall(self, col, row):
        self.__field[row][col].unsetWall()

    def getReward(self, col, row):
        return self.__field[row][col].getReward()

    def setReward(self, col, row, newReward):
        self.__field[row][col].setReward(newReward)

    def isWall(self, col, row):
        return self.__field[row][col].isWall()

    def isAbsorber(self, col, row):
        return self.__field[row][col].isAbsorber()

    def getBestDirection(self, col, row):
        return self.__field[row][col].getBestDirection()

    def setBestDirection(self, col, row, newBestDirection):
        return self.__field[row][col].setBestDirection(newBestDirection)
